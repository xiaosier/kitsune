# This docker file assumes a bunch of things happen in terms of volumes and
# ports. See start.sh for more details.
FROM mythmon/python-dev
MAINTAINER #sumodev

# Install system deps
RUN apt-get install -y nodejs npm

# This assumes that the runner put the git repo here.
# This only works with the running docker though, not at build time, so...
VOLUME /kitsune
WORKDIR /kitsune

# ...also copy critical build files for build time.
ADD package.json /kitsune/package.json

RUN pwd
RUN ls /kitsune -la

# Install JS deps
RUN npm install
# Install Python deps

# This will always be run.
ENTRYPOINT ["/kitsune/manage.py"]
# These are the default parameters to the above, and may be overwritten.
CMD ["runserver"]
