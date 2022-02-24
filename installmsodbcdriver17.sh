#!/bin/bash

# import the public repository GPG keys
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

# register the Microsoft Ubuntu repository
# Debian 11
curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# update the sources list and run the installation command with the unixODBC developer package
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql17
# optional: for bcp and sqlcmd
ACCEPT_EULA=Y apt-get install -y mssql-tools
# make sqlcmd/bcp accessible from the bash shell for interactive/non-login sessions
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
# optional: for unixODBC development headers
apt-get install -y unixodbc-dev
# optional: kerberos library for debian-slim distributions
# sudo apt-get install -y libgssapi-krb5-2