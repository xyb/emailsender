#!/bin/bash

python manage.py migrate
python manage.py collectstatic --noinput

python manage.py runserver 0.0.0.0:8000 &

sleep 1
echo

python manage.py purge_mail_log 30

python manage.py runmailer &
echo

wait -n

exit $?
