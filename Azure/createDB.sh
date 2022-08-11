sudo su postgres <<EOF
psql -c 'CREATE DATABASE azure;'
EOF
exit

-- Database: azure

-- DROP DATABASE IF EXISTS azure;

CREATE DATABASE azure
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
