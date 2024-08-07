## Social Networking API
## Overview
    This project provides an API for a social networking application using Django Rest Framework. It includes functionalities for user authentication, user search, and friend request management.

## Prerequisites
    Docker
    Docker Compose

## Getting Started
    1. Clone the Repository
        git clone https://github.com/sridevicheekatla/SocialMedia.git
        cd socialmedia
    2. Build and Run the Containers
        a. docker-compose up --build
           This command will build the Docker images and start the containers as defined in the docker-compose.yml file.

    3. Migrate the Database

        Run the following command to apply the initial migrations:
        a. docker-compose run web python manage.py makemigrations socialmedia_app
        b. docker-compose run web python manage.py migrate socialmedia_app
        c. docker-compose run web python manage.py migrate
        d. docker-compose run web python manage.py createsuperuser(optional)
        e. docker-compose up
