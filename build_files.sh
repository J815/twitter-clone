# build_files.sh
pip install -r requirements.txt
cd twitting 
python manage.py collectstatic
