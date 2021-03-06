from django.core.exceptions import ValidationError
from rest_framework import serializers, viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from kitsune.questions.models import Question, Answer
from kitsune.sumo.api import CORSMixin, OnlyCreatorEdits


class QuestionShortSerializer(serializers.ModelSerializer):
    # Use slugs for product and topic instead of ids.
    product = serializers.SlugRelatedField(required=True, slug_field='slug')
    topic = serializers.SlugRelatedField(required=True, slug_field='slug')
    # Use usernames for creator and updated_by instead of ids.
    creator = serializers.SlugRelatedField(
        slug_field='username', required=False)
    updated_by = serializers.SlugRelatedField(
        slug_field='username', required=False)

    class Meta:
        model = Question
        fields = (
            'id',
            'created',
            'creator',
            'is_archived',
            'is_locked',
            'is_spam',
            'last_answer',
            'locale',
            'num_answers',
            'num_votes_past_week',
            'product',
            'title',
            'topic',
            'updated_by',
            'updated',
        )

    def validate_creator(self, attrs, source):
        user = getattr(self.context.get('request'), 'user')
        if user and not user.is_anonymous() and attrs.get('creator') is None:
            attrs['creator'] = user
        return attrs


class QuestionDetailSerializer(QuestionShortSerializer):
    class Meta:
        model = Question
        fields = QuestionShortSerializer.Meta.fields + (
            'content',
            'answers',
        )


class QuestionViewSet(CORSMixin, viewsets.ModelViewSet):
    serializer_class = QuestionDetailSerializer
    queryset = Question.objects.all()
    paginate_by = 20
    permission_classes = [
        OnlyCreatorEdits,
        permissions.IsAuthenticatedOrReadOnly,
    ]
    filter_backends = [
        filters.DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filter_fields = [
        'creator',
        'created',
        'is_archived',
        'is_locked',
        'is_spam',
        'locale',
        'num_answers',
        'product',
        'title',
        'topic',
        'updated',
        'updated_by',
    ]
    ordering_fields = [
        'id',
        'created',
        'last_answer',
        'num_answers',
        'num_votes_past_week',
        'updated',
    ]
    # Default, if not overwritten
    ordering = ('-id',)

    def get_pagination_serializer(self, page):
        """
        Return a serializer instance to use with paginated data.
        """
        class SerializerClass(self.pagination_serializer_class):
            class Meta:
                object_serializer_class = QuestionShortSerializer

        context = self.get_serializer_context()
        return SerializerClass(instance=page, context=context)

    @action(methods=['POST'])
    def solve(self, request, pk=None):
        """Accept an answer as the solution to the question."""
        question = self.get_object()
        answer_id = request.DATA.get('answer')

        try:
            answer = Answer.objects.get(pk=answer_id)
        except Answer.DoesNotExist:
            return Response({'answer': 'This field is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        question.set_solution(answer, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerShortSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field='username',
                                           required=False)
    updated_by = serializers.SlugRelatedField(slug_field='username',
                                              required=False)

    class Meta:
        model = Answer
        fields = (
            'id',
            'question',
            'created',
            'creator',
            'updated',
            'updated_by',
        )

    def validate_creator(self, attrs, source):
        user = getattr(self.context.get('request'), 'user')
        if user and not user.is_anonymous() and attrs.get('creator') is None:
            attrs['creator'] = user
        return attrs


class AnswerDetailSerializer(AnswerShortSerializer):
    class Meta:
        model = Answer
        fields = AnswerShortSerializer.Meta.fields + (
            'content',
        )


class AnswerViewSet(CORSMixin, viewsets.ModelViewSet):
    serializer_class = AnswerDetailSerializer
    queryset = Answer.objects.all()
    paginate_by = 20
    permission_classes = [
        OnlyCreatorEdits,
        permissions.IsAuthenticatedOrReadOnly,
    ]
    filter_backends = [
        filters.DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filter_fields = [
        'question',
        'created',
        'creator',
        'updated',
        'updated_by',
    ]
    ordering_fields = [
        'id',
        'created',
        'updated',
    ]
    # Default, if not overwritten
    ordering = ('-id',)

    def get_pagination_serializer(self, page):
        """
        Return a serializer instance to use with paginated data.
        """
        class SerializerClass(self.pagination_serializer_class):
            class Meta:
                object_serializer_class = AnswerShortSerializer

        context = self.get_serializer_context()
        return SerializerClass(instance=page, context=context)
