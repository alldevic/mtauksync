#! /usr/bin/env sh

set -o errexit
set -o pipefail

if [[ ${DEBUGPY} == 'TRUE' ]] || [[ ${DEBUGPY} == 'True' ]] || [[ ${DEBUGPY} == '1' ]]; then
    echo >&2 "Starting debug server with debugpy..."
    python3 -m debugpy --listen 0.0.0.0:5678 \
        -m uvicorn mtauksync.asgi:application \
            --host 0.0.0.0 \
            --port 8000 \
            --access-log \
            --use-colors \
            --log-level info \
            --lifespan off \
            --reload &
fi

function postgres_ready() {
    python3 <<END
import sys
import psycopg2
from os import environ
def get_env(key, default=None):
    val = environ.get(key, default)
    if val == 'True':
        val = True
    elif val == 'False':
        val = False
    return val
try:
    dbname = get_env('POSTGRES_DB')
    user = get_env('POSTGRES_USER')
    password = get_env('POSTGRES_PASSWORD')
    host = get_env('POSTGRES_HOST')
    port = 5432
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
    echo >&2 "Postgres is unavailable - sleeping"
    sleep 1
done

echo >&2 "Postgres is up - continuing..."

function mt_mysql_ready() {
    python3 <<END
import sys
from MySQLdb import _mysql
from os import environ
def get_env(key, default=None):
    val = environ.get(key, default)
    if val == 'True':
        val = True
    elif val == 'False':
        val = False
    return val
try:
    dbname = get_env('MT_MYSQL_DB')
    user = get_env('MT_MYSQL_USER')
    password = get_env('MT_MYSQL_PASSWORD')
    host = get_env('MT_MYSQL_HOST')
    port = 3306
    conn = _mysql.connect(dbname=dbname, user=user, passwd=password, host=host, port=port)
except:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
    echo >&2 "MT MySQL is unavailable - sleeping"
    sleep 1
done

echo >&2 "MT MySQL is up - continuing..."

echo >&2 "Migrating..."
python3 manage.py migrate

echo >&2 "Collect static..."
python3 manage.py collectstatic --noinput

echo >&2 "Init schedule tassk"
python3 manage.py inittasks

if [[ ${DEBUGPY} == 'TRUE' ]] || [[ ${DEBUGPY} == 'True' ]] || [[ ${DEBUGPY} == '1' ]]; then
    wait
elif [[ ${DEBUG} == 'TRUE' ]] || [[ ${DEBUG} == 'True' ]] || [[ ${DEBUG} == '1' ]]; then
    echo >&2 "Starting debug server..."
    exec python3 -m uvicorn mtauksync.asgi:application \
            --host 0.0.0.0 \
            --port 8000 \
            --access-log \
            --use-colors \
            --log-level info \
            --lifespan off \
            --reload
else
    echo >&2 "Starting Gunicorn..."
    exec gunicorn mtauksync.asgi:application \
        -k uvicorn.workers.UvicornWorker \
        --access-logfile - \
        --name mtauksync \
        --bind 0.0.0.0:8000 \
        --workers=3
fi
fi
