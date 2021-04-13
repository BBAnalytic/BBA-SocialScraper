# Specify the base image
FROM ubuntu:18.04

# Specify language being used.
FROM python:3

# Create a working directory. 
WORKDIR /app

# Creating environment variables:
ENV FLASK_APP=api.py

# Copying files from this directory to the container's WORKDIR directory
COPY ./requirements.txt .

# Installing requirements
RUN pip install -r requirements.txt

# Copy everything into the WORKDIR
COPY . .