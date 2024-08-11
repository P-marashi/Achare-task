## How to use it ?

### declaring Environment variable for Django debug:
Cause of usage of the debug variable before env initialization, template needs the debug variable from environment and you can set it in linux os with the command below:

```export DJANGO_DEBUG=true```

The value of this variable can be true/false

### Running tests

for ensure it is working as well, you can run command below in the root of project:

```pytest```

### Running makemigrations & migrate

```python manage.py makemigrations```

```python manage.py migrate```

### Run project with Docker

you can run project with docker with this command

#TODO: COMPLETE HERE AT THE END