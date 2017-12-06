FROM ubuntu

# Install updates
RUN apt-get update

# Install curl
RUN apt-get install python python-pip python-dev python-numpy -y
RUN pip install coremltools tensorflow h5py keras numpy protobuf

# Copy server
COPY ./ /app
WORKDIR /app
