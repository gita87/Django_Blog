Blogging Website made with Django


1. **Clone Repository:**
   ```bash
   git clone https://github.com/gita87/Django_Blog.git
   ```

2. **Copy Environment Variables Sample:**
   ```bash
   cp .env.sample .env
   ```

3. **Run Docker Compose:**
   ```bash
    docker-compose -f docker-compose.prod.yml up -d
   ```

4. **Access the Application:**
   - Open your web browser.
   - Navigate to the corresponding address and port specified in your Docker setup. Typically, it might be [http://localhost:8000/](http://localhost:8000/).

These steps assume that the repository contains a Dockerized Django application, and the `docker-compose.yml` file is configured to run the application. Adjust the commands and URLs based on your specific project structure and configurations.