# upc2017
Backend for UPC 2017

---

# [oscar](https://plentsov.com/)

![Preview](https://plentsov.com/images/twist-representive.png)

## About
**Advanced analytics used easily in a conversation**

* Talk to your database like a human: _We use advanced natural language processing techniques to create world class conversational experience_
* Get data insights like you never did before: _It’s never been so easy to identify factors that impact customers’ engagement and revenue._
* Smart AI-based database understanding: _No complex setup required 
It's never been so easy to get advanced statistics_
* Inside your favorite messaging app: _One-click integration with Twist gives you more time to do stuff that matters._

## Tech

TL;DR [Stackshare](https://stackshare.io/oscarupc/oscarupc)

Our app consists of four main parts:

* Backend; Here we use microservice based approach with services build using **Golang** and **Python**. 
* DevOps; We use **AWS EC2** as our infrastructure provider. All our microservices are running using **supervisor** to provide demonization and easy restart/logging access. We use **AWS Route53** for DNS related things. Every app is running behind **nginx** reverse proxy. 
* AI; We use two frameworks. **CatBoost** for Python implementing gradient boosting on decision trees with a native support of categorical features and **GoML** for Golang to perform sentiment analysis via Naive Bayes classification.
* Frontend; We have build responsive landing page using **ES6/Bootstrap/jQuery**

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
        
