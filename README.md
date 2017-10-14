# upc2017
Backend for UPC 2017

---

# Commands:

### /oscar help
  returns all possible commands with descriptions

### /oscar plot
  returns a picture that vizualizes the given query

### /oscar query
  returns data that mathches the given query

# How to deploy

Use deploy.sh script in the root directory. You should have private key called `key.pem` in your .ssh directory and following line in your ssh config:
```
Host upc
        HostName ec2-18-194-130-70.eu-central-1.compute.amazonaws.com
        User ec2-user
```
        
