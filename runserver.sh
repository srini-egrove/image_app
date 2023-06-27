echo
echo
echo "===> Installing pip packages!"
pip install -r requirements.txt
echo
echo
echo "===> Running the developement server"
python manage.py runserver 0.0.0.0:8000
