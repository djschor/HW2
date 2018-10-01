## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, flash, url_for, redirect
import requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, DateField, IntegerField, BooleanField, ValidationError # see some new ones... + ValidationError
from wtforms.validators import Required, Length
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'
app.debug=True

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
    name = StringField("Enter the name of an album: ", validators=[Required(),Length(3,64)]) # Must be at least 3 and no more than 64 chars
    ranking = RadioField('How much do you like the album? (1 low, 3 high)', choices = ['1', '2', '3'])
    submit = SubmitField("Submit")

####################

@app.route('/')
def hello_world():
####################
###### ROUTES ######
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/music/<music>')
def getstuff(music): 
	baseurl = "https://itunes.apple.com/search" 
	params_diction = {}
	params_diction["term"] = music
	resp = requests.get(baseurl, params=params_diction)
	text = resp.text
	return text

@app.route('/artistform')
def artistform():
	return render_template('artistform.html')

@app.route('/artistinfo',methods=["GET"])
def result_artform():
    if request.method == "GET":
        print("ARGUMENTS", "     ", request.args) # Check out your Terminal window where you're running this...
        baseurl = "https://itunes.apple.com/search"
        params_diction = {}
        artiste = request.args.get('artist','')
        params_diction["term"] = artiste
        resp = requests.get(baseurl, params=params_diction)
        text = resp.text
        data = json.loads(text)
        objects = []
        for item in data['results']:
        	if 'trackName' in item:
        		objects.append(item)
        return render_template('artist_info.html', objects=objects)

    return "Nothing was selected this time!"

@app.route('/artistlinks',methods=["GET"])
def links(): 
	return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def specific(artist_name):
    baseurl = "https://itunes.apple.com/search"
    params_diction = {}
    params_diction["term"] = artist_name
    resp = requests.get(baseurl, params=params_diction)
    text = resp.text
    data = json.loads(text)
    results = []
    for item in data['results']:
    	if 'trackName' in item:
    		results.append(item)
    return render_template('specific_artist.html', results=results)

@app.route('/album_entry')
def form_entry():
    form = AlbumEntryForm()
    return render_template('/album_entry.html', form=form)
 
@app.route('/album_data', methods = ['GET', 'POST'])
def show_answers():
    form = AlbumEntryForm()
    if form.validate_on_submit():
        name = form.name.data
        ranking = form.ranking.data
        return render_template('album_data.html',name=name,ranking=ranking)
    flash(form.errors)
    return redirect(url_for('/form_entry'))


if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
