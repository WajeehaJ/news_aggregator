# news_aggregator
## Installation Commands for Window 10 PowerShell:

```
pip  install virtualenv
mkdir dev
cd dev
ls
pwd
mkdir news_aggregator_proj
cd news_aggregator_proj
virtualenv .
.\Scripts\activate
pip install django==2.1.7
pip install newsapi-python
pip install praw
```
## Downloading the code from Wajeeha Javed GitHub Repo 

Go to the following link to download the Code
https://github.com/WajeehaJ/news_aggregator.git

and copy the src folder to your news_aggregator_proj folder. 


## Running the News-Aggregator

```
cd src
django-admin startproject newsAggregator
django-admin startapp news_collector 
python manage.py runserver 
```
## Running the News-Aggregator Unit Tests

python manage.py test news_collector