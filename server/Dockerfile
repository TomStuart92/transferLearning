FROM ubuntu

# Install updates
RUN apt-get update

# Install curl
RUN apt-get install python python-pip python-dev python-numpy -y
RUN pip install mock flask

# Install tensorflow
RUN pip install tensorflow

# Copy server
COPY ./ /app
WORKDIR /app
EXPOSE 5000
CMD FLASK_APP=server.py flask run --host=0.0.0.0
