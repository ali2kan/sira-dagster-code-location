FROM python:3.11-slim

# Define build arguments
ARG PIPELINE_NAME=pipeline_y
ARG GRPC_PORT=4001

# Set environment variables
ENV PIPELINE_NAME=${PIPELINE_NAME}
ENV GRPC_PORT=${GRPC_PORT}

# Checkout and install dagster libraries needed to run the gRPC server
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Add repository code
WORKDIR /opt/dagster/app/
RUN mkdir /opt/dagster/app/${PIPELINE_NAME}

COPY . /opt/dagster/app/${PIPELINE_NAME}

# Run dagster gRPC server on specified port
EXPOSE ${GRPC_PORT}

# CMD allows this to be overridden from run launchers or executors that want
# to run other commands against your repository
CMD ["sh", "-c", "dagster api grpc -h 0.0.0.0 -p ${GRPC_PORT} -m ${PIPELINE_NAME}"]
