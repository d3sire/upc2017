ssh -i ~/.ssh/upc.pem upc "cd /home/www && sudo git pull origin master && sudo env "PATH=$PATH" supervisorctl restart oscar"
