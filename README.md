# covid19-forecasting plots

A simple Plotly Dash application that displays plots for various stages of hospitalization

PI: Michael C. Hughes

## Usage

Configurations are stored in plot/config.json

### Two workflows are supported:
* View the charts by running a Plotly Dash app (using a local webserver)
* Embed the Plotly graphs in an html page

### Run the Plotly Dash app:

```
$ python application.py
```

Visit: 
[http://127.0.0.1:8050/](http://127.0.0.1:8050/)

### Embed the Plotly graphs in an html page
```
$ python plot.py --dash False
```

The plots are available in plot/dashboard.html

## Deployment to AWS ElasticBeanstalk

### Prerequisites:
* Create an AWS account.
* Create an Identity and Access Management (IAM) role with AWSElasticBeanstalkFullAccess.
* Install the EasticBeanstalk CLI: https://github.com/aws/aws-elastic-beanstalk-cli-setup.

### Forward
Now you'll be all ready to read the instructions for Flask deployment for EBS (Dash uses Flask under the hood). Their instructions assume you are creating the app as you go, in this case you have your app all ready to deploy. There are optional steps to allow ssh access to the instance(s), I would advice against it. When creating your virtual env to test locally you should use python 3.6.10 (the lastest ebs currently supports). If you choose to make any sort of env that lives in the project directory do not forget to add it to the gitignore and ebsignore.

### Instructions
Follow the instructions for Flask deployment for EBS:
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html.


## Summary



## Install

#### 1. Install Plotly Dash

```
pip install dash==1.10.0
```
