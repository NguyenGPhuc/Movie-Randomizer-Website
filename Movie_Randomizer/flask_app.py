from flask import Flask, render_template, redirect
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

my_key = 'ef955c2e'

# Random names that use to generate first 5 movies.
deault_title = ["Battle", "End", "World", "War", "Sea", "Transform", "Blade", "Flower", "Dog", "Cat"]
random_default_title = random.sample(deault_title, 1)
print(random_default_title)

# USE https://www.omdbapi.com/ to see what parameter can be use.
payload = {
  'apikey': my_key,
#   't': 'Iron Man'
    's': random_default_title,
  'type': 'movie',
#   'page': 2
}

endpoint = "http://www.omdbapi.com/?"

# This 
try:
  r = requests.get(endpoint, params=payload)
  data = r.json()

  movie_list = list(data['Search'])
  shuffle_list = random.sample(movie_list,6)
#   pprint(shuffle_list[0]['Poster'])

#   print movie_list, np.random.shuffle(movie_list)
#   pprint(movie_list)
#   data = dict(movie_list)
#   print(data['Search'][0])
    # print(next(iter(data.values())))
#   print(data['Title'])
#   pprint(data['TotalResult'])

#   urllib.request.urlretrieve(shuffle_list[0]['Poster'], "poster_0.jpg")
#   img = Image.open("poster_0.jpg")
#   img.show()
except:
  print('please try again')



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
        store_movie(form.movie_title.data)
        return redirect('/detail')


    return render_template('home.html', form=form, image_data_0 = shuffle_list[0],
                            image_data_1 = shuffle_list[1], image_data_2 = shuffle_list[2],
                            image_data_3 = shuffle_list[3], image_data_4 = shuffle_list[4])


# Detail of specific movie when clicked (WIP)
@app.route('/detail')
def detail():
    return render_template('detail.html', listOfMovie=listOfMovie)