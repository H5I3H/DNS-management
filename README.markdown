# Binder #

This is final project of NTU NASA 2016.

A Django web application for viewing and editing BIND DNS zone records.

Binder supports adding and deleting DNS records (I am working on editing right now). TSIG-authenticated transfers and updates are supported.

The original code is at [here](http://github.com/jforman/binder).

## Installation ##

There are some build dependencies for the Python mondules, on apt based systems these can be installed with

    apt-get install python-dev libxml2-dev libxslt-dev git

Initial checkout has to be performed with git

    git clone https://github.com/jforman/binder.git

### Requirements ###

Once the git repository has been cloned these can be installed with one command

    pip install -r requirements.txt

Packages installed:

* [Django](http://www.djangoproject.com) >=1.8
* Python Modules
  * [pybindxml](https://pypi.python.org/pypi?name=pybindxml&:action=display): This is a shared library for scraping and sticking into Python dict objects various server/zone data from a BIND DNS server.
  * Beautifulsoup4: This library is included as a dependency of pybindmlx when you install pybindxml.
  * [python-dnspython](http://www.dnspython.org/)
  * [python-sqlite](http://docs.python.org/2/library/sqlite3.html) (If you will be using Sqlite for server and key storage)

Elsewhere you will need a [Bind DNS Server](http://www.isc.org/software/bind) running (at least version 9.5.x, which provides instrumentation for gathering process and zone statistics remotely).

To verify that required and optional dependencies are installed, execute [check-dependencies.py](https://github.com/H5I3H/DNS-management/blob/master/check-dependencies.py). This script checks that various Python modules will import correctly.

## Configuration ##

### binder/ ###

If you wish to override anything from settings.py it should be done in a new file

* local_settings.py: Local settings called by Binder templates for TTL choices, record types handled, etc.

### config/ ###

Provided under the config directory are various example configurations for runing Binder:

* binder-apache.conf.dist: Name-based virtual host configuration for running Binder under Apache.
* django.wsgi: WSGI configuration file called by Apache to run Binder.
* binder-nginx.conf.dist: Name-based virtual host configuration for running Binder under Nginx using fcgi.
* binder-upstart.conf.dist: Ubuntu Upstart configuration file for starting Binder upon machine startup.

These are not necesary for development but are useful once moving to production.

### Admin user ###

It is necesary to create an administrative user

    python manage.py createsuperuser

## Running Binder ##
The development server is run as most Django dev servers are run.

    /opt/binder/manage.py migrate
    /opt/binder/manage.py runserver

Once you have the Django server up and running, you will want to configure at least one BIND server in the Django Admin app. This includes a hostname, TCP statistics port and a default TSIG transfer key to be used when doing AXFR actions (if necessary).

Keys should also be created, if needed. The name of the key should match the contents of the below noted key file. Along side the name, key data and type should also be specified.

Once these two pieces of configuration are done, open up [http://yourserver:port/](http://yourserver:port) to access Binder and begin DNS zone management.

## BIND DNS Server ##

When Binder accesses your BIND DNS server, it first queries the statistics port to gather zone information. This includes zone name, view, and serial number. This is all configured by some of the following configuration examples.

#### named.conf ####

We must provide server statistics from the BIND process itself. This allows Binder to query BIND itself and get a list of zones, views, and other statistics.

    options {
      zone-statistics yes;
    }

    statistics-channels {
        inet * port 8053 allow { 10.10.0.0/24; };
    };

This tells bind to start an HTTP server on port 8053 on all interfaces, allowing 10.10.0.0/24 to make requests on this interface, http://${bind_server}:8053/. You will most likely want to narrow down the subset of hosts or subnets that can query BIND for this data. This data can be viewed via your choice of Browser, or read by your favorite programming language and progamatically processed by your choice of XML library.

    include "/etc/bind/dynzone.key";

This tells Bind to load a TSIG key from dynzone.key that can be referenced later in named.conf.

Moving on to zone declaration, determine how locked down you want zone updates and transfers to be. The following zone is defined to allow all zone transfers, but restrict updates to those provided with the dynzone-key TSIG key.

    zone "dynzone.yourdomain.org" IN {
        type master;
        file "/var/cache/bind/master/db.dynzone.yourdomain.org";
        allow-update { key dynzone-key; };
    };

#### /etc/bind/dynzone.key ####

Below are the entire contents of the dynzone.key file. This specifies the name, algorith and TSIG secret.

    key dynzone-key {
        algorithm hmac-md5;
        secret "foobar...BhBrq+Ra3fBzhA4IWjXY85AVUdxkSSObbw3D30xgsf.....";
    };

referenced as 'dynzone-key' in named.conf

For information on TSIG see http://www.cyberciti.biz/faq/unix-linux-bind-named-configuring-tsig/ .
