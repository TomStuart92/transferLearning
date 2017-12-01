FROM ubuntu

# Install updates
RUN apt-get update
RUN apt-get install -y --no-install-recommends apt-utils

# Install curl
RUN apt-get install curl -y
RUN apt-get install python python-pip python-dev python-numpy -y
RUN pip install mock flask

# Install tensorflow
RUN pip install tensorflow

# Copy server
COPY ./ /app
WORKDIR /app
CMD FLASK_APP=server.py flask run
