#!/bin/bash

FILE_NAME=his.bak
DATABASE_NAME=his
SQL_SERVER_CONTAINER_NAME=`docker-compose ps sqlserver | tail -n +3 | awk '{ print $1 }'`
WEB_CONTAINER_NAME=`docker-compose ps web | tail -n +3 | awk '{ print $1 }'`

# SQL Server
docker exec $SQL_SERVER_CONTAINER_NAME mkdir -p /var/opt/mssql/backup
docker cp ./sqlserverbackupdata/$FILE_NAME $SQL_SERVER_CONTAINER_NAME:/var/opt/mssql/backup
docker exec $SQL_SERVER_CONTAINER_NAME /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P '<YourStrong@Passw0rd>' \
    -Q "DROP DATABASE IF EXISTS $DATABASE_NAME; RESTORE DATABASE $DATABASE_NAME FROM DISK = '/var/opt/mssql/backup/$FILE_NAME' WITH FILE = 1, NOUNLOAD, STATS = 5"

# PostgreSQL
docker exec -it $WEB_CONTAINER_NAME python manage.py makemigrations
docker exec -it $WEB_CONTAINER_NAME python manage.py migrate