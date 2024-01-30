# build_files.sh
pip install -r requirements.txt
python ./twitting/manage.py collectstatic
