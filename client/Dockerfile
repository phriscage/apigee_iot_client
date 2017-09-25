###############################################################################
##  Name:   Dockerfile
##  Date:   2017-09-24
##  Developer:  Chris Page
##  Email:  phriscage@gmail.com
##  Purpose:   This Dockerfile contains the IoT EnviroPhat client
################################################################################
FROM container4armhf/armhf-alpine:3.6
# required for py-smbus
#FROM container4armhf/armhf-alpine:edge

# Set the file maintainer (your name - the file's author)
MAINTAINER Chris Page <phriscage@gmail.com>

# Set the application directory
WORKDIR /app

# Add our requirements.txt
ADD requirements.txt /app/requirements.txt

# Add CA Certificates for remote packages
RUN apk add ca-certificates

# Install dependencies for Python3
RUN apk --update add build-base python3 python3-dev && \
	ln -fs /usr/bin/python3 /usr/bin/python && \
	# Install our requirements.txt
	pip3 install -r requirements.txt && \
	apk del build-base && \
  	rm -rf /var/cache/apk/*

# workaround until https://github.com/pimoroni/enviro-phat is updated for python3 smbus
RUN sed -i 's/import smbus/import smbus2 as smbus/' /usr/lib/python3.6/site-packages/envirophat/i2c_bus.py

## Let's add all the examples into the /app directory for now
ADD . /app/.

CMD ["python", "main.py"]
