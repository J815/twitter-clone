set -e
set -x
echo "install requirements.txt"
pip install -r requirements.txt
echo "change directory"
cd twitting
echo "migrate "
python manage.py migrate 

# if [[ $CREATE_SUPERUSER ]];
# then
echo "create superuser "
python manage.py createsuperuser --no-input
# fi
