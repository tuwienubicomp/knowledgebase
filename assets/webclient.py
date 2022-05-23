import urequests          # library used for making HTTP requests
from time import sleep
response = urequests.get('http://jsonplaceholder.typicode.com/albums/1') # make a GET request to the url
print(type(response))     # print statements for debugging differen ways to interact with the response and its body
print(response.text)
print(type(response.text))
sleep(1)
response_json = response.json()
print(type(response_json))
print(response_json)
sleep(1)
print(response_json['id'])
print(response_json['title'])
print(response_json['userId'])

