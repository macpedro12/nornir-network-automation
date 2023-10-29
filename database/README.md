# How to start the PostgresSQL database on a Docker Container.

1. Enter the database/ folder
2. Execute the command 'docker-compose up --build' (If image don't exist) or 'docker-compose up'
The --build flag will make sure that the container receives the .sql script and create the table.

The postgres database will accept local connections (localhost) on the port 5432. [TODO] Analyse if it is viable to change the listen-address conf.

### Dockerfile

Currently using postgres:16-alpine3.18 and copying the create_tables.sql to the container, so it can be executed on start.

### docker-compose.yml

Run the PostgresSQL container using the modified image and creates the volume dbdata.
The variables are stored in .env file.

### create_tables.sql

Create the table I'll be iniatilly using in this project.

## Linux Requirements

1. libpq-dev 
2. python-dev
3. python3
4. docker-compose
5. docker