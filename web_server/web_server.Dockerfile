# Use an official Python runtime as a parent image
FROM python:3-stretch
# define encoding
ENV PYTHONIOENCODING UTF-8
# Set the working directory to /app - this is a directory that gets created in the image
WORKDIR /app
# Copy the current host directory contents into the container at /app
COPY . /app/
# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
# Map port 8080 to flask port 5000
EXPOSE 8080:5000
# Run greeter_server.py when the container launches
CMD ["python", "web_server.py"]