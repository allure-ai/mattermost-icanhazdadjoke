from flask import Flask, request
import random
import requests

app = Flask(__name__)

@app.route('/joke/mattermost', methods=['POST'])
def search_joke():
    search_query = request.form.get('text')

    if not search_query:
        joke = fetch_single_joke()
    else:
        joke = fetch_search(search_query)

    return {
        "response_type": "in_channel",
        "text": joke,
        "username": "allure-joker",
        "icon_url": "https://allure.id/assets/img/favicon.png"
    }

def fetch_single_joke():
    r = requests.get('https://icanhazdadjoke.com/', headers={'Accept': 'application/json'})
    joke = r.json()

    return joke['joke']


def fetch_search(search_query):
    r = requests.get('https://icanhazdadjoke.com/search', headers={'Accept': 'application/json'}, params={'term': search_query})
    jokes = r.json()['results']

    if len(jokes) == 0:
        return "No joke found"
    
    joke = random.choice(jokes)
    return joke['joke']
