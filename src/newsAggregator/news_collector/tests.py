from django.test import TestCase
from django.test import Client
import json

class BasicTestCases(TestCase):
	def setUp(self):
		self.client = Client() 

	def testGetNewsResponse(self):
		response = self.client.get('/news/')
		self.assertEqual(response.status_code,200)

	def testSearchNewResponse(self):
		response = self.client.get('/news/?query="bitcoin"')
		self.assertEqual(response.status_code,200)

     
	def testSearchEmptyQuery(self):
		response = self.client.get('/news/?query=')
		self.assertEqual(response.status_code,200)
		
	def testSearchInvalidQuery(self):
		response = self.client.get('/news/?query="@34222!"')
		json_response = response.json()
		if json_response.find("status:'400'") > 0:
			pass
			
	

