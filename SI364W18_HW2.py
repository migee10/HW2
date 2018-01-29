## SI 364
## Winter 2018
## HW 2 - Part 1

#Michele Gee
## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required

import requests
import json

# http://localhost:5000/artistform -> artistform.html
# http://localhost:5000/artistinfo -> artist_info.html
# http://localhost:5000/artistlinks -> artist_links.html
# http://localhost:5000/specific/song/<artist_name> -> specific_artist.html
#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

class AlbumEntryForm(FlaskForm):
    name = StringField('Enter the name of an album:', validators=[Required()])
    options = RadioField('How much do you like this album?', choices=[('1','1'),('2','2'),('3','3')], validators=[Required()])
    submit = SubmitField('Submit')
# /album_entry, which should render the WTForm you just created (note that there
# is a raw HTML form in one of the provided templates, but THIS should rely on your
# WTForms form). It should send data to a template called album_entry.html (see Part 3).
# The form should look pretty much like this when you are done with Part 3.
#
# /album_result, which should render the results of what was submitted to the
# AlbumEntryForm, like this when you are done with Part 3. It should send data to
# a template called album_data.html (see Part 3).
class ArtistForm(FlaskForm):
    artist = StringField('Enter Artist to search for:', validators = [Required()])
    submit = SubmitField('Submit')

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/user/<name>')
def helloser(name):
    return'<h1> Hello {0} <h1>'.format(name)



@app.route('/album_entry')
def albumentry():
    albumEntryForm = AlbumEntryForm()
    return render_template('album_entry.html', form=albumEntryForm)

@app.route('/album_result', methods = ['POST'])
def album_result():
    # get title and score from args
    # pass album as param to template
    title = request.form['name']
    score = request.form['options']
    album = {}
    album['title'] = title
    album['score'] = score
    return render_template('album_data.html', album = album )


@app.route('/artistform')
def artistform():
    simpleForm = ArtistForm()
    return render_template('artistform.html', form=simpleForm)

@app.route('/artistinfo')
def artistinfo():
    artist = request.args['artist']
    params = {}
    params['term'] = artist
    response = requests.get('https://itunes.apple.com/search', params=params)
    results = json.loads(response.text)['results']
    return render_template('artist_info.html', objects = results)
        #print(response)
        #print(results)



@app.route('/artistlinks')
def artistlink():
    return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def specificartist(artist_name):
    params = {}
    params['term'] = artist_name
    response = requests.get('https://itunes.apple.com/search', params=params)
    results = json.loads(response.text)['results']
    print(response)
    print(results)
    return render_template('specific_artist.html', results = results)


####################
###### FORMS #######
####################




####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello<h1>'.format(name)


if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
