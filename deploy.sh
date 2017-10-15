ssh -i ~/.ssh/upc.pem upc "cd /home/www && sudo git pull origin master && sudo `which pip3` install -r requirements.txt && sudo env "PATH=$PATH" supervisorctl restart oscar"
