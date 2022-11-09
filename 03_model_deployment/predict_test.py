import requests
import json

url = 'http://localhost:9698/predict'
# url = "{url_from_cloud_run}/predict"

with open('03_model_deployment/song.json') as song_json:
    song = json.load(song_json)

print(requests.post(url, json=song))
result = requests.post(url, json=song).json()

print(result)