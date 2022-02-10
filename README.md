# Setup

Database:

```sql
CREATE DATABASE evisa_backend CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_cs;
CREATE USER 'evisa_backend'@'%' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON evisa_backend.* TO 'evisa_backend'@'%';
FLUSH PRIVILEGES;
```


### Production setup
```
pip install -r main/requirements/prod.txt
```

Additional Nginx configuration:
```
server {
    client_max_body_size 50M;
}
```

### Development setup
```
pip install -r main/requirements/dev.txt
```

### Running tests
```
coverage run
coverage html && xdg-open ./htmlcov/index.html
```

### Check coding style
https://www.flake8rules.com/
```
flake8
```
