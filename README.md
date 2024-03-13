Blogging Website made with Django


1. **Clone Repository:**
   ```bash
   git clone https://github.com/gita87/Django_Blog.git
   ```

2. **Copy Environment Variables Sample :**
   ```bash
   cp .env.sample .env
   ```

3. **Build Docker Containers :**
   ```bash
   docker-compose up -d --build
   ```

4. **Create Superuser :**
   ```bash
   docker exec -it django-blog-template-web sh -c "/app/venv/bin/python /app/manage.py createsuperuser"
   ```

5. **Access the Application:**
   - Open your web browser.
   - Navigate to the corresponding address and port specified in your Docker setup. Typically, it might be [http://localhost:1337/](http://localhost:1337/).