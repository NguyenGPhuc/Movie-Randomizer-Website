from flask import Flask, request, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
from pprint import pprint
from PIL import Image

import requests, json
import random
from random import shuffle
import numpy as np
import urllib.request

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'csumb-otter'

def searchAPI(title):
  my_key = 'ef955c2e'

  # Random names that use to generate first 5 movies.
  deault_title = ["Battle", "End", "World", "War", "Sea", "Transform", "Avenger", "Flower", "Dog", "Cat", "Love"]
  random_default_title = random.sample(deault_title, 1)
  print(random_default_title)

  if not title:
    movie_title = random_default_title
  else:
    movie_title = title

  print ("In search API")

  # USE https://www.omdbapi.com/ to see what parameter can be use.
  payload = {
    'apikey': my_key,
    's': movie_title,
    'type': 'movie',
  }

  endpoint = "http://www.omdbapi.com/?"

  # This 
  try:
    r = requests.get(endpoint, params=payload)
    data = r.json()

    movie_list = list(data['Search'])
    shuffle_list = random.sample(movie_list,6)

    return shuffle_list
  except:
    print('please try again')

# searchAPI('')

def callAPI(id):
  my_key = 'ef955c2e'

  print ("In call API")

  payload = {
  'apikey': my_key,
  'i': id,
  'plot': 'full'
  }

  endpoint = "http://www.omdbapi.com/?"

  # This 
  try:
    r = requests.get(endpoint, params=payload)
    data = r.json()

    print (data['Ratings'][0]['Source'])
    print (data['Ratings'][0]['Value'])
    print (data['Plot'])

    return data
  except:
    print('please try again')

  
callAPI('tt3896198')

class MovieList(FlaskForm):
    movie_title = StringField('Movie Title',
    validators=[DataRequired()]
    )

listOfMovie = []

def store_movie(my_movie):
    listOfMovie.append(dict(
        movie = my_movie,
        date = datetime.today()
    ))


# Home route show 5 movies poster (WIP)
@app.route('/', methods=('GET', 'POST'))
def home():
    form = MovieList()
    if form.validate_on_submit():
        global keyword_title 
        keyword_title = form.movie_title.data
        return redirect('/movie_detail')

    shuffle_list = searchAPI('')

    return render_template('home.html', form=form, image_data = shuffle_list)

@app.route('/movie_detail')
def movie_detail():
  
  payload = {
    'apikey': 'ef955c2e',
    's': keyword_title,
    'type': 'movie',
  }
  endpoint = "http://www.omdbapi.com/?"

  try:
      r = requests.get(endpoint, params=payload)
      data = r.json()
      print(data)
      size = len(data['Search'])
  except:
      print('please try again')

  return render_template('movie_detail.html', data=data, size=size)

# Detail of specific movie when clicked (WIP)
@app.route('/detail/<id>')
def detail(id):

  # print (id['Ratings']['Metascore'])
  selected_id = callAPI(id)
  print (selected_id['Ratings'])
  return render_template('detail.html', selected_id = selected_id)
