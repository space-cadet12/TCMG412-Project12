# Use an official Python runtime as a parent image
FROM python:3.9.7

# Set up a working directory in /app
#basically sets up a VM then cd /app in the VM
WORKDIR /app

# Copy your Flask app into the working dir
COPY . /app

# Install any needed Python packages with pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 4000 available to the world outside this container
EXPOSE 4000

# Run app.py when the container launches
CMD ["python3", "Project_9_API.py"]

#####
#command to use this file as insturctions
#tag is the name


#docker build flask-app
#docker run -p 8080:5000 flask.app
#####

#####
#download the redis image before building the container 
#RUN docker pull redis:latest

#allow for the use of an empty password
#RUN docker run --name redis_cont    \
#    -e ALLOW_EMPTY_PASSWORD=yes \
#    bitnami/redis:latest
    
#Bind the redis port when running docker (port was originally 6379:6379)

#RUN docker run -p 80:80 –name redis_cont -d redis
#RUN docker run -p 6379:6379 –name redis_cont -d redis

#bind a local volume for persistent redis data (port originally 6379:6379)
#RUN docker run -p 80:80 -d                  \
#    -v $PWD/redis-data:/bitnami/redis/data  \
#    --name redis_cont                       \
#    bitnami/redis:latest 
# <-- Redis image

#Start redis server.
#RUN redis-cli 

#to confirm it is running
#RUN redis-cli ping

#If the previous docker run command returns an invalid reference format error, try removing the -name tag or use the redis:latest command to pull from the latest image
#RUN docker run -p 5000:5000/tcp -d redis:latest (port originally 6379:6379)
#####

#####
# Grab the redis server image 
#RUN docker pull redis:latest

# Create the local dockernet to run the API and the sever on so they can talk to each other 
#RUN docker network create team_1_net

# Set the server to run in the background (while the container is being run it will run in background i think)
#RUN docker -d --rm --network team_1_net -p 6379:6379 --name redis-server redis:latest

# Set the API to run once server is up (I don't think this is how you would do it acutally)
#RUN docker run --rm --network team_1_net -p 4000:4000 Project_9_API_Container
#####