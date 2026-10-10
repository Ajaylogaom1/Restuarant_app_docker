# 🍴 The Good Food — Dockerized Restaurant Website

A restaurant website deployment project built using **Python, MySQL, Nginx, Docker, and Docker Compose**. The application displays restaurant dishes, prices, descriptions, and images, with additional menu items retrieved from a MySQL database.

This project demonstrates containerization, multi-container orchestration, reverse proxy configuration, database integration, and cloud deployment using AWS EC2.

## 🚀 Project Overview

The application is containerized using Docker and runs as three services managed by Docker Compose:

* **Python:** Serves the restaurant website and retrieves additional dishes from MySQL.
* **MySQL:** Stores restaurant menu data.
* **Nginx:** Acts as a reverse proxy and exposes the website on HTTP port 80.

## 🏗️ Architecture

```text
                 User / Web Browser
                         |
                         v
                   AWS EC2 Server
                         |
                    Port 80 (HTTP)
                         |
                         v
                  +-------------+
                  |    Nginx    |
                  +-------------+
                         |
                         v
                  +-------------+
                  | Python App  |
                  +-------------+
                         |
                         v
                  +-------------+
                  |    MySQL    |
                  +-------------+
                         |
                         v
                    Menu Data
```

The services communicate through a Docker network configured in Docker Compose.

## 🛠️ Technologies Used

* Linux (Ubuntu)
* Docker
* Docker Compose
* Python 3.13
* MySQL
* Nginx
* AWS EC2
* HTML, CSS, and JavaScript
* Git and GitHub

## ✨ Features

* Restaurant landing page and navigation
* Menu cards displaying dishes, descriptions, prices, and images
* Shopping cart interface
* Additional dishes retrieved from MySQL
* Separate containers for the application, database, and reverse proxy
* Persistent database storage using a Docker volume
* Multi-container deployment using Docker Compose
* Cloud hosting on AWS EC2

## 📁 Project Structure

```text
project/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── README.md
├── nginx/
│   ├── Dockerfile
│   └── default.conf
└── static/
    ├── style.css
    └── script.js
```

*Note: Adjust the folder structure above to match your actual repository before publishing.*

## ⚙️ Prerequisites

Install the following on your machine or server:

* Docker Engine
* Docker Compose plugin
* Git
* An AWS EC2 Ubuntu instance (for cloud deployment)

## 🚀 Run the Project Locally

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_REPOSITORY_NAME
```

### 2. Configure environment variables

Configure the MySQL database name, username, password, and application connection settings in your Docker Compose configuration or environment file.

Keep passwords and other secrets out of GitHub. Use your own secure credentials.

### 3. Build and start the containers

```bash
docker compose up --build -d
```

### 4. Check the containers

```bash
docker compose ps
```

### 5. View application logs

```bash
docker compose logs -f
```

To view individual services:

```bash
docker compose logs python
docker compose logs nginx
docker compose logs db
```

### 6. Access the website

Open the following URL in your browser:

```text
http://localhost
```

If deployed on AWS EC2, open:

```text
http://YOUR_EC2_PUBLIC_IP
```

Ensure the EC2 security group permits inbound HTTP traffic on port 80.

## 🗄️ Database Management

The MySQL container stores restaurant menu information. The Python application retrieves additional dishes from the database.

Connect to MySQL using:

```bash
docker compose exec db mysql -u root -p
```

Select your configured database and inspect its tables:

```sql
SHOW DATABASES;
USE your_database_name;
SHOW TABLES;
```

Replace `your_database_name` with the actual database name configured for your project.

Database persistence depends on the volume configuration in `docker-compose.yml`. Avoid deleting database volumes when stopping or rebuilding containers.

## 🔧 Useful Docker Commands

| Task                                 | Command                         |
| ------------------------------------ | ------------------------------- |
| Start services                       | `docker compose up -d`          |
| Build and start                      | `docker compose up --build -d`  |
| View containers                      | `docker compose ps -a`          |
| Follow logs                          | `docker compose logs -f`        |
| Stop services                        | `docker compose down`           |
| Rebuild an image                     | `docker compose build python`   |
| Open a shell in the Python container | `docker compose exec python sh` |

## ☁️ AWS EC2 Deployment

1. Launch an Ubuntu EC2 instance.
2. Install Docker Engine and the Docker Compose plugin.
3. Clone the project repository.
4. Configure the database credentials and environment variables.
5. Build and start the containers using Docker Compose.
6. Verify container health and application logs.
7. Configure the EC2 security group to allow inbound HTTP traffic on port 80.
8. Access the restaurant website using the EC2 public IPv4 address.

For security, do not expose the MySQL port publicly unless there is a specific requirement. Prefer allowing database access only within the Docker network.

## 🔐 Security Considerations

* Do not commit `.env` files containing credentials.
* Exclude database files and local development data from the Git repository.
* Use strong database passwords.
* Avoid exposing MySQL directly to the internet.
* Restrict AWS security group rules to the required ports.
* Use HTTPS and a trusted TLS certificate for a production deployment.

## 📚 What I Learned

* Writing Dockerfiles to containerize an application
* Creating and managing multiple services with Docker Compose
* Connecting Python applications to MySQL
* Configuring Nginx as a reverse proxy
* Using Docker networks for service communication
* Persisting database data with volumes
* Troubleshooting container startup and database connection issues
* Deploying a containerized application on AWS EC2
* Managing project files with Git and GitHub

## 🔮 Future Improvements

* Add a CI/CD pipeline using GitHub Actions
* Add application health checks
* Implement HTTPS with a trusted TLS certificate
* Add monitoring and centralized logging
* Improve database initialization and backup procedures

## 👨‍💻 Author

Created as a hands-on DevOps and cloud deployment learning project.

**Focus:** Docker, Docker Compose, Linux, MySQL, Nginx, and AWS EC2.

