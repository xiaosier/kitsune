# This docker file assumes a bunch of things happen in terms of volumes and
# ports. See start.sh for more details.
FROM mythmon/python-dev
MAINTAINER #sumodev

# Install system deps
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get install -y python-software-properties software-properties-common
RUN add-apt-repository ppa:chris-lea/node.js
RUN apt-get update
RUN apt-get install -y nodejs

# This assumes that the runner put the git repo here.
# This only works with the running docker though, not at build time, so...
VOLUME /kitsune
WORKDIR /kitsune

# ...also copy critical build files for build time.
COPY package.json /kitsune/package.json

RUN pwd
RUN ls /kitsune -la

# Install JS deps
RUN npm install

# Install Python deps
# TODO

# This will always be run.
ENTRYPOINT ["/kitsune/manage.py"]
# These are the default parameters to the above, and may be overwritten.
CMD ["runserver"]
