set -o errexit
pip install -r requirements.txt

cd twitting

python manage.py migrate 

if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input
fi