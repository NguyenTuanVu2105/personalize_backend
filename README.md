## PrintHolo

B1: Build base image chứa các package

```$ docker build -f Dockerfile.Base -t pip-requirements-installed-image:latest .```

B2: Build các service dựa trên base image bên trên

```$ docker-compose build web ```

```$ docker-compose build celery-worker ```

```$ docker-compose build celery-beat ```

```$ docker-compose build payment_processor```

B3: Chạy hệ thống

```$ docker-compose up -d```

## Export DATA trong posgres

```docker exec -it your_container_id pg_dump -U postgres -w -C -F p fulfillment-hub > hub.sql```

Import Data

Tạo DB fulfillment-hub

```psql -U postgres

select pg_terminate_backend(pid) from pg_stat_activity where datname='fulfillment-hub';

drop database "fulfillment-hub";

create database "fulfillment-hub";

```

Xóa hết các bảng trong DB

Chạy lệnh migrate nếu chưa migrate

```python manage.py migrate```

Chạy lệnh

```cat fulfill_init.sql | docker exec -i your_container_id psql -U postgres fulfillment-hub```

## DEPLOY 


Edit biến môi trường như trong file .env

Build ảnh docker với file .Dockerfile 



