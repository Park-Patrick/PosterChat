# Posterchat DB Wiki

## Table of Contents

- [Posterchat DB Wiki](#posterchat-db-wiki)
  - [Setting up the Posterchat DB](#setting-up-the-posterchat-db)
  - [How PosterChat is Connected to Postgres](#how-posterchat-is-connected-to-postgres)

## Setting up the Posterchat DB

This document outlines how to deploy a local Postgresql db to use for development. For dev, we use the official Postgresql container as our actual instance of Postgres, and Adminer as a management interface.

1. First make sure docker-ce and docker-compose are installed. We use docker to ensure that the dev environment is consistent across computers. We don't want unit tests to only fail for some developers, simply because of how they might have their environment set up.

https://docs.docker.com/compose/install/

2. In the shell, navigate to the same directory as the docker compose file

```
(pc) seranthirugnanam@MBP001 db_utils % pwd
/Users/seranthirugnanam/Documents/Develop/PosterChat/db_utils
(pc) seranthirugnanam@MBP001 db_utils % ls
docker-compose.yml
```

3. Docker isolates the environment that Postgres runs in from your OS (except for some portions of the kernel). This means that inside the container, Postgres will have its own filesystem. Postgres, by default, expects files in the following location:
   `/var/lib/postresql/data`
   We will need to provide a volume mount which tells Docker where we want the Postgres container to save any data. We use docker volumes for this.

```
(pc) seranthirugnanam@MBP001 db_utils % docker volume ls
DRIVER              VOLUME NAME
local               1b472dec98f674f2621cbe65da4a2f3b5c79b18aeb29908dd7e2057643d39bc6
local               e4626506ad1c6af60aacc4057528f792f9b18ca229ddbfe4795d65905aa76794
```

Running the above commands showing me all available volume mounts. By default Docker doesn't use a human-friendly string. That's why when you look in the docker-compose.yml file, you will see this line:

```
volumes:
  db_data:
```

And in the `db` service of the docker-compose.yml file you will see:

```
volumes:
      - db_data:/var/lib/postresql/data
```

This is telling Docker that we want to create a shared volume called "db*data' (a human-friendly name) and map it to where Postgres expects data to be stored \_inside* the container.

4. Before we run the container, we need to specify some environment variables. Add the following environment variables to your system (I'm on a Mac so this is in ~/.zshrc)

```
# POSTCHAT CONFIG
export POSTERCHAT_DB_NAME="posterchat_dev" # The name of the posterchat database
export POSTERCHAT_DB_USER="admin" # Your default admin username
export POSTERCHAT_DB_PASSWORD="admin" # Your default admin pass
export POSTERCHAT_DB_HOST="localhost" # Where your DB is hosted
export POSTERCHAT_DB_PORT="5432" # The port to allocate for Postgres
```

5. Once your environment variables are updated and sourced you can start the service

```
# From same directory as docker-compose.yml file
(pc) seranthirugnanam@MBP001 db_utils % pwd
/Users/seranthirugnanam/Documents/Develop/PosterChat/db_utils
(pc) seranthirugnanam@MBP001 db_utils % ls
docker-compose.yml
(pc) seranthirugnanam@MBP001 db_utils % docker-compose up -d
Creating network "db_utils_default" with the default driver
Creating volume "db_utils_db_data" with default driver
Creating db_utils_adminer_1 ... done
Creating db_utils_db_1      ... done
(pc) seranthirugnanam@MBP001 db_utils %
```

6. At this point your DB is up and running. We can also verify our volume mount via the following:

```
(pc) seranthirugnanam@MBP001 db_utils % docker volume ls
DRIVER              VOLUME NAME
local               1b472dec98f674f2621cbe65da4a2f3b5c79b18aeb29908dd7e2057643d39bc6
local               a5eb213cfce568c97f72cd16b3e30cb21ed0180c975462cb9b5fb4ea8d4a0690
local               db_utils_db_data
local               e4626506ad1c6af60aacc4057528f792f9b18ca229ddbfe4795d65905aa76794)
```

You can see above that I have a new volume called "db_utils_db_data". Docker prefixes the name of the volume with "db_utils" because thats the folder my docker-compose.yml is in. "db_data" is the name given to the volume in the docker-compose.yml

7. In the browser, you should be able to navigate to the Adminer interface: http://localhost:8080
   For the login:
   System: Postgres
   Server: db
   Username: # Whatever you specified for POSTERCHAT_DB_USER in your environment variables
   Password: # Whatever you specified for POSTERCHAT_DB_PASSWORD in your enviornment variables
   Database: # Whatever you specified for POSTERCHAT_DB_NAEM in your environment variables

Once logged in you will see blank tables and views

8. Now we can run any migrations on our new DBs
   In PosterChat's Django project:

```
/Users/seranthirugnanam/Documents/Develop/PosterChat
(pc) seranthirugnanam@MBP001 PosterChat % ls
Procfile                core                    manage.py               poster                  requirements.txt        staticfiles
README.md               db_utils                media                   posterchat              runtime.txt             templates
(pc) seranthirugnanam@MBP001 PosterChat % python manage.py migrate
Operations to perform:
  Apply all migrations: account, admin, auth, contenttypes, core, guardian, poster, sessions, sites, socialaccount
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK

  ...

  Applying socialaccount.0003_extra_data_default_dict... OK
```

Refresh the Adminer webpage and you will see everything migrated in

9. We can even use this development DB for running unit tests

```
(pc) seranthirugnanam@MBP001 PosterChat % python manage.py test core
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.EEEEFFFF
```

Unit tests failed (because of dev errors) but Django created a new DB for us, ran our unit tests against it, then deleted the DB afterwards. It didn't mess with any data inside of the local database since it creates a new DB for running unit tests.

10. You can stop the local Postergres server using the following command from the docker-compose.yml directory

```
(pc) seranthirugnanam@MBP001 db_utils % ls
docker-compose.yml
(pc) seranthirugnanam@MBP001 db_utils % docker-compose down
Stopping db_utils_adminer_1 ... done
Stopping db_utils_db_1      ... done
Removing db_utils_adminer_1 ... done
Removing db_utils_db_1      ... done
Removing network db_utils_default
(pc) seranthirugnanam@MBP001 db_utils %
```

11. When you start the db again, your data will still be there

```
(pc) seranthirugnanam@MBP001 db_utils % ls
docker-compose.yml
(pc) seranthirugnanam@MBP001 db_utils % docker-compose up -d
Creating network "db_utils_default" with the default driver
Creating db_utils_adminer_1 ... done
Creating db_utils_db_1      ... done
```

12. If you want to complete delete your Postgres DB data you can delete the Docker volume:

```
(pc) seranthirugnanam@MBP001 db_utils % ls
docker-compose.yml
(pc) seranthirugnanam@MBP001 db_utils % docker-compose down
Stopping db_utils_adminer_1 ... done
Stopping db_utils_db_1      ... done
Removing db_utils_adminer_1 ... done
Removing db_utils_db_1      ... done
Removing network db_utils_default
(pc) seranthirugnanam@MBP001 db_utils % docker volume ls
DRIVER              VOLUME NAME
local               1b472dec98f674f2621cbe65da4a2f3b5c79b18aeb29908dd7e2057643d39bc6
local               db_utils_db_data
local               e4626506ad1c6af60aacc4057528f792f9b18ca229ddbfe4795d65905aa76794
(pc) seranthirugnanam@MBP001 db_utils % docker volume rm db_utils_db_data
db_utils_db_data
(pc) seranthirugnanam@MBP001 db_utils % docker-compose up -d
Creating network "db_utils_default" with the default driver
Creating volume "db_utils_db_data" with default driver
Creating db_utils_adminer_1 ... done
Creating db_utils_db_1      ... done
```

When the service is restarted, it will be wiped and you will need to run Django migrations again

```
(pc) seranthirugnanam@MBP001 PosterChat % python manage.py migrate
Operations to perform:
  Apply all migrations: account, admin, auth, contenttypes, core, guardian, poster, sessions, sites, socialaccount
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK

  ...


  Applying socialaccount.0001_initial... OK
  Applying socialaccount.0002_token_max_lengths... OK
```

## How PosterChat is Connected to Postgres

PosterChat uses PostgreSQL in the backend. Below are implementation details on how this was set up.

Connection details are specified via environment variables. When we go to deploy, we will simply point the server to the correct database via environment variables. The same can be done in a dev environment.

The reason behind this is so that there are minimal changes in the code when changing which database we would like our Django application to point to. All you need to do is modify your environment variables. For this demonstration I will show how to point Django to our instance of PostgreSQL running in the cloud.

1. Add relevant environment variables specified in settings.py.

Below you can see this is what is present in settings.py

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("POSTERCHAT_DB_NAME"),
        'USER': os.getenv("POSTERCHAT_DB_USER"),
        'PASSWORD': os.getenv("POSTERCHAT_DB_PASSWORD"),
        'HOST': os.getenv("POSTERCHAT_DB_HOST"),
        'PORT': os.getenv("POSTERCHAT_DB_PORT"),
    },
    "TEST": {
        "NAME": "test_posterchat" # Used for running unit tests
    }
}
```

So on my system (MacOS/Linux) I just need to add the environment variables to my path.

```
# POSTCHAT CONFIG
export POSTERCHAT_DB_NAME="<db_name>"
export POSTERCHAT_DB_USER="<db_user>"
export POSTERCHAT_DB_PASSWORD="<db_password>"
export POSTERCHAT_DB_HOST="<db_host>"
export POSTERCHAT_DB_PORT="<db_port>"
```

2. If this is a new database instance, we need to use the usual Django migration steps

```
(pc) seranthirugnanam@MBP001 PosterChat % python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, poster, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying poster.0001_initial... OK
  Applying sessions.0001_initial... OK
```

And that should be it. If you want to point to a different database, just change the environment variables and run again.
