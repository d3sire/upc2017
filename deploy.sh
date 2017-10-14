ssh -i ~/.ssh/upc.pem upc "cd /home/www && sudo git pull origin master && sudo pip-3.4 install -r requirements.txt && sudo env "PATH=$PATH" supervisorctl restart oscar"
