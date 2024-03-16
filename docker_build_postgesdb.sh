docker run -d \
  -e POSTGRES_USER=blog_username \
  -e POSTGRES_PASSWORD=bl0g_p4ssw0rd \
  -e POSTGRES_DB=blog_db \
  -p 5434:5432 \
  --name blog_postgres_container \
  postgres:latest
