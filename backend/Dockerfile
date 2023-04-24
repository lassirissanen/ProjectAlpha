# Use an official Python runtime as a parent image 
FROM python:3.10.8-slim-buster

# Set the working directory to /app 
WORKDIR /app

# Copy the current directory contents into the container at /app 
COPY . /app 

# Install libvoikko and copy the python file to app
RUN apt-get update && apt-get install -y voikko-fi python-libvoikko
RUN cp /usr/lib/python3/dist-packages/libvoikko.py /app/libvoikko.py

# Install any needed packages specified in requirements.txt 
RUN pip install --trusted-host pypi.python.org -r requirements.txt


# Make port 5000 available to the world outside this container 
EXPOSE 5000

# Run app.py when the container launches 
CMD ["python", "backend.py"]