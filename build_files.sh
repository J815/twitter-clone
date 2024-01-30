# build_files.sh
pip install -r requirements.txt
python ./twitting/twitting/manage.py collectstatic
