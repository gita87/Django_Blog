Blogging Website made with Django


1. **Clone Repository:**
   ```bash
   git clone https://github.com/gita87/Django_Blog.git
   ```

2. **Copy Environment Variables Sample:**
   ```bash
   cp .env.sample .env
   ```

3. **Build Docker Postgre:**
   ```bash
   sh docker_build_postgesdb.sh
   ```

4. **Activate Virtual Environment and Install Package :**
   ```bash
   python3 -m venv venv
   source ./venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Create a migration and a superuser :**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Run Gunicorn:**
   ```bash
   gunicorn --bind 0.0.0.0:8000 blog_project.wsgi:application
   ```

5. **Access the Application:**
   - Open your web browser.
   - Navigate to the corresponding address and port specified in your Docker setup. Typically, it might be [http://localhost:8000/](http://localhost:8000/).