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
RUN apt-get install -y libmysqlclient-dev libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev

# This assumes that the runner put the git repo here.
# This only works with the running docker though, not at build time, so...
VOLUME /kitsune
WORKDIR /kitsune

# ...also copy critical build files for build time.
ADD package.json /kitsune/package.json
ADD requirements/compiled.txt /kitsune/requirements/compiled.txt

# Install JS deps
RUN npm install

# Install Python deps
RUN pip install -r requirements/compiled.txt

EXPOSE 8000

# These are the default command to run, but it can be overwritten.
CMD ["/kitsune/manage.py", "runserver"]
