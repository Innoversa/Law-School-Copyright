import requests
import json

class spotifyAPI:
	def __init__(self):
		self.creds = {
			'client_id': 'f4027d8eec9f4f5c9b9febfdb0a0f87b',
			'client_secret': '584c419c5fce45798e504ee8ce0b9969',
			'grant_type': 'client_credentials',
		}
		self.tokenURL = 'https://accounts.spotify.com/api/token'
		self.token = ''
		self.refreshToken()
		self.searchURL = 'https://api.spotify.com/v1/search'
		self.lastQuery = ''
		self.lastResult = ''
	#access token expires after 3600 seconds, or one hour.
	def refreshToken(self):
		intermediate = requests.post(self.tokenURL, data=self.creds)
		self.token = intermediate.json()['access_token']

	def query(self,queryString):
		self.lastQuery = queryString
		self.lastResult = requests.get(
			self.searchURL,
			headers={ 'Authorization': 'Bearer ' + self.token },
			params={ 'q': queryString, 'type': 'track' }
		)
		

#Below is for testing only

#myAPI = spotifyAPI()
#myAPI.query('Take me home, Country Roads')
#print(myAPI.lastResult.json())







#Below is trash old code used for debugging
#creds = {
#	'client_id': 'f4027d8eec9f4f5c9b9febfdb0a0f87b',
#	'client_secret': '584c419c5fce45798e504ee8ce0b9969',
#	'grant_type': 'client_credentials',
#}
#
#url = 'https://accounts.spotify.com/api/token'
#	
#x = requests.post(url, data=creds)
#
#aut = x.json()['access_token']
#
#searchUrl = "https://api.spotify.com/v1/search"
#
#x2 = requests.get(
#    searchUrl,
#    headers={ 'Authorization': 'Bearer ' + aut },
#    params={ 'q': 'Take me home, country roads', 'type': 'track', 'artist': 'John Denver' })
#print(x2)
#print(x2.text)
#print('8')
#print(x2.json())