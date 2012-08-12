service_list = [
    # venv
    # memecache
    # gunicorn
    # git
    # nginx
    # mysql
    {"action":"run", "params":"whoami"},
    {"action":"sudo", "params":"apt-get update", "message":"Updating apt-get"},
    {"action":"apt",
        "params":["mysql-client", "libmysqlclient-dev", "nginx", "memcached", "git",
        "python-setuptools", "python-dev", "build-essential", "python-pip", "python-mysqldb"],
        "message":"Installing apt-get packages"},
]