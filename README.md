# Digtial Attendance Application - API v2

## Introduction
Digital Attendance is an open-source project supported by UNICEF Kenya through a collaboration with [Sisitech](https://sisitech.com). The platform allows tracking of individual student attendance in schools.

It is comprised of three components:
- **API**: Django Rest Framework (this project)
- **Dashboard**: Angular Web Application 
- **Application**: Ionic Hybrid Application 

## Digital Attendance Journey
- [Digital Attendance Journey Journey](https://drive.google.com/file/d/17T3VT-howD86XOSYrExLVMXWiXTiXimD/view)

## User Manual
- [Onekana User Manual](https://sisitech.github.io/OnekanaDocs/)

---

# Pre-Built Docker image
[sisitechdev/daa-v2-api](https://hub.docker.com/r/sisitechdev/daa-v2-api)


# Docker Compose 

```yaml
version: "3.8"
services:
  
  nginxmedia:
    image: nginx:1.15
    networks:
      - db
    ports:
      - 8888:80

    volumes:
      - media:/usr/share/nginx/media
      - static:/usr/share/nginx/static
      - ./nginx.conf:/etc/nginx/conf.d/default.conf

  api:
    image: sisitechdev/daa-v2-api:v1.0.0 # Location with a Dockerfile
    restart: always
    depends_on:
      - db
      - memcached
    networks:
      - db
    volumes:
      - media:/media
      - static:/static

    environment:
      SECRET_KEY: test_secret_key
      DB_PASSWORD: test_password
      DB_USER: moeke
      DB_NAME: moekeapi 
      DB_HOST: db
      MEDIA_ROOT: /media
      STATIC_ROOT: /static
      MEDIA_URL: http://localhost:8888/media/
      STATIC_URL: http://localhost:8888/static/
      DOCS_TITLE: Digital Attendance Application API
      DOCS_SUB_TITLE: API Docs
      DOCS_LOGO: https://www.unicef.org/sites/default/files/styles/logo/public/English_9.png.webp?itok=KaPGNxiU

    ports:
      - 8020:8000
    
    
  
  background_tasks:
    image: sisitechdev/daa-v2-api:v1.0.0 # Location with a Dockerfile
    restart: always
    command: python manage.py process_tasks

    depends_on:
      - db
      - memcached
      - api
    
    networks:
      - db
    volumes:
      - media:/media
      - static:/static

    environment:
      SECRET_KEY: test_secret_key
      DB_PASSWORD: test_password
      DB_USER: moeke
      DB_NAME: moekeapi 
      DB_HOST: db

  
  memcached:
    image: memcached:latest
    ports:
      - "11211:11211"
    
    networks:
      - db


  db:
    image: postgres
    restart: always
    networks:
      - db
    environment:
      POSTGRES_PASSWORD: test_password
      POSTGRES_USER: moeke
      POSTGRES_DB: moekeapi
    volumes:
      - pg:/var/lib/postgresql/data

    
networks:
  db:

volumes:
  pg:
  media:
  static:
```
### API Documentation
After the API is up and running, the documentation is served at the root URL:  
[API Docs](http://localhost:8020)


# Setup Guide

## Prerequisites

- Python 3.8 or higher
- Git
- A virtual environment tool like `venv` or `virtualenv`
- PostgreSQL (for database setup)

## Setup Instructions

### 1. Clone the Repository

Start by cloning the project repository from GitHub:

```bash
git clone https://github.com/unicefkenya/daa-api-v2.git
cd daa-api-v2
```

### 2. Create a Virtual Environment

Create and activate a virtual environment for the project using Python 3.8 or above:

```bash
# For Unix/Mac
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

With the virtual environment activated, install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root of the project with the following content:

```env
SECRET_KEY="your_secret_key"
ALLOWED_HOSTS="localhost,api.domain.com"
DOCS_TITLE="Onekana"
DOCS_SUB_TITLE="API Docs"
DOCS_LOGO="https://path/to/logo.png"
DB_NAME="your_database_name"
DB_USER="your_database_user"
DB_PASSWORD="your_database_password"
DB_HOST="your_database_host"
DB_PORT=5432

# For storing media files
USE_S3=true # or false
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
AWS_STORAGE_BUCKET_NAME=""
AWS_S3_REGION_NAME=""
AWS_S3_ENDPOINT_URL=""

AWS_STATIC_LOCATION="" # folder name inside the bucket
AWS_MEDIA_LOCATION="" # folder name inside the bucket

# If using file storage
STATIC_ROOT=""
STATIC_URL=""

MEDIA_ROOT=""
MEDIA_URL=""
```

Replace the placeholder values (e.g., `your_secret_key`, `your_database_name`) with your actual configuration details.

### 5. Run Tests

To ensure everything is set up correctly, run the project's tests:

```bash
python manage.py test
```

If the tests pass successfully, your environment is ready!

### 6. Create a Superuser

Run the following command to start the process of creating a superuser.
```bash
python manage.py createsuperuser
```

Docker
```
docker exec -it <container_id> python manage.py createsuperuser
```


### 7. Adding Reasons for Absence and Deletion in Django Admin

To add and manage the "reason for absence" and "reason for deletion" options, follow these steps in the Django admin panel:

1. **Access the Django Admin:**
   Log in to the Django admin panel. Ensure you have the necessary permissions to manage these options.

2. **Navigate to the Relevant Model:**
   In the Django admin dashboard, locate the models for managing "Reasons for Absence" and "Reasons for Deletion".

3. **Add or Edit Options:**
   For each of these models, add or edit the available reasons. Ensure that an option with name **"other"** is included. The **"other"** option will trigger the mobile application to present a text field for additional input.

   Setup in the admin panel:
   - **Reason for Absence Options:**
     - Sick
     - Family Emergency
     - Transportation Issues
     - other (Description: "Select this option to enter a custom reason")

   - **Reason for Deletion Options:**
     - Transferred
     - Graduated
     - Dropped Out
     - other (Description: "Select this option to enter a custom reason")

##  Want to Contribute or Have Any Questions?
We welcome contributions and feedback! If you want to contribute to this project or have any questions, reach out via email at hello@sisitech.com


