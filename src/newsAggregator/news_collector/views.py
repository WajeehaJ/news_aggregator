
from django.http import HttpResponse
from django.shortcuts import render
from newsapi import NewsApiClient
# Create your views here.
from newsapi import NewsApiClient
import json
from django.http import JsonResponse 
import praw
import re 

#function to check if the string is valid and does not contains special characters
def is_valid_string(var):
	return ((type(var) == str) and len(var) < 512 and re.match("^[a-zA-Z0-9_]*$", var))

#index page of the django server
def home_view(request):
	return render(request, "Welcome.html", {})

#
def news_view(request):
	#extracting url parameter 'query' with request.GET
	search_str = request.GET.get('query', '') 
	list_data = []
	#Use News API Client for invoking the News API calls
	#TODO: make API key configurable
	newsapi = NewsApiClient(api_key='0defc751cb8b421dae67e870b611185b')

    #Use PRAW Wrapper for accessing the Reddit API
    #TODO: Make PRAW parameter configurable  	
	reddit = praw.Reddit(client_id='9of88qFNAaRcpg', client_secret="DyEFroEw-sdfvVEhsQECRFYcYto", \
    						password='wajeehaalvi123', user_agent='wajeeha', username='wajeeha123') 
	
	if not is_valid_string(search_str):
           return JsonResponse("{message: 'String cannot have special characters and should be type string', status: '400'}", safe=False)
	#if it query search string is empty then will retrieve only general news
	#TODO: make the limit of the search results configurable  
	if not search_str.strip(): 
		top_headlines = newsapi.get_top_headlines(language='en', country='us')
		subreddit =  reddit.subreddit('news')
		top_headlines_redditapi = subreddit.top(limit=27)
	else:
		top_headlines = newsapi.get_everything(q=search_str, language='en')
		subreddit =  reddit.subreddit('all')
		top_headlines_redditapi = subreddit.search(search_str, sort="new",limit=27)

    #if the top headlines from newsapi exists and the status attribute is ok 
	if (top_headlines['articles']) and (top_headlines['status'] == "ok"): 
		#parse through the top headlines and extract title, url attributes     
		for content in top_headlines['articles']:
			response_dict = dict()
			response_dict['headlines'] = content['title']
			response_dict['link'] =  content ['url']
			response_dict['source'] = "newsapi"
			list_data.append(response_dict)
	

	if top_headlines_redditapi:
		#parse through the top headlines and extract title, url attributes
		for content in top_headlines_redditapi:
			response_dict = dict()
			response_dict['headlines'] = content.title
			response_dict['link'] =  content.url
			response_dict['source'] = "redditapi"
			list_data.append(response_dict)
	
	#if Search Results are Empty 				
	if not list_data:
		return JsonResponse("{message: 'No Results found', status: '404'}", safe=False)

	return HttpResponse(json.dumps(list_data, sort_keys=True, indent=4), content_type="text/json-comment-filtered")



