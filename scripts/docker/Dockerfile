# This docker file assumes a bunch of things happen in terms of volumes and
# ports. See start.sh for more details.
FROM mythmon/python-dev
MAINTAINER #sumodev

# This assumes that the runner put the git repo here.
WORKDIR /kitsune

# This will always be run.
ENTRYPOINT ["/kitsune/manage.py"]
# These are the default parameters to the above, and may be overwritten.
CMD ["runserver"]
