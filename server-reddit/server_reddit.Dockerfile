# Use an official Python runtime as a parent image
FROM python:3-stretch
# Set the working directory to /app - this is a directory that gets created in the image
WORKDIR /app
# Copy the current host directory contents into the container at /app
COPY . /app
# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
# Make port 9998 available outside this container
EXPOSE 9998
# Run greeter_server.py when the container launches
CMD ["python", "server_reddit.py"]
