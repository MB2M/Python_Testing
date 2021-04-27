import json
import datetime

from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

@app.template_filter('is_past')
def is_past(value, format="%Y-%m-%d %H:%M:%S"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return True
    if datetime.datetime.strptime(value, format) > datetime.datetime.now():
        return False


competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
    except:
        flash("Sorry, that email was not found.")
        return redirect(url_for('index'))
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    if placesRequired > int(club['points']):
        flash('Sorry, you dont have the required points')
        return redirect(url_for('book', competition=competition['name'], club=club['name']))
    elif placesRequired > 12:
        flash('Sorry, you can not redeem more than 12 points')
        return redirect(url_for('book', competition=competition['name'], club=club['name']))
    elif datetime.datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S") < datetime.datetime.now():
        flash('Sorry, past competition cannot be booked')
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        club['points'] = int(club['points']) - placesRequired
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/board', methods=['GET'])
def board():
    return render_template('board.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))