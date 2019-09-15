
from django.http import HttpResponse
from django.shortcuts import render
from newsapi import NewsApiClient
# Create your views here.
from newsapi import NewsApiClient
import json
from django.http import JsonResponse 
import praw 

def news_view(request):
	#extracting url parameter 'query' with request.GET
	search_str = request.GET.get('query', '') 
	list_data = []
	newsapi = NewsApiClient(api_key='0defc751cb8b421dae67e870b611185b')
	#if it is not Null then retrieve only general news 
	if not search_str: 
		top_headlines = newsapi.get_top_headlines(language='en', country='us')
	else:
	    top_headlines = newsapi.get_everything(q=search_str, language='en')

	#parse through the top headlines and extract title, url attributes     
	for content in top_headlines['articles']:
		response_dict = dict()
		response_dict['headlines'] = content['title']
		response_dict['link'] =  content ['url']
		response_dict['source'] = "newsapi"
		list_data.append(response_dict)

	#Use PRAW Wrapper for accessing the Reddit API 	
	reddit = praw.Reddit(client_id='9of88qFNAaRcpg', client_secret="DyEFroEw-sdfvVEhsQECRFYcYto", \
    						password='wajeehaalvi123', user_agent='wajeeha', username='wajeeha123') 
	if not search_str: 
		subreddit =  reddit.subreddit('news')
		top_headlines_redditapi = subreddit.top(limit=27)
	else: 
		subreddit =  reddit.subreddit('all')
		top_headlines_redditapi = subreddit.search(search_str, limit=27)


	
	for content in top_headlines_redditapi:
		response_dict = dict()
		response_dict['headlines'] = content.title
		response_dict['link'] =  content.url
		response_dict['source'] = "redditapi"
		list_data.append(response_dict)		

	return HttpResponse(json.dumps(list_data, sort_keys=True, indent=4), content_type="text/json-comment-filtered")


# Create your views here.
