from app import *
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from forms import *
from db_models_setup import *
from datetime import *

#  ----------------------------------------------------------------  
#  Read: Dispaly a list of all venues
#  ----------------------------------------------------------------
@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  resultData = []

  # find all the states from Venue table
  states = Venue.query.with_entities(Venue.state, func.count(Venue.city)).group_by(Venue.state).all()

  # Loop through each state
  for oneState in states:

    # all the cities for one state
    stateCitys = Venue.query.filter(Venue.state==oneState[0]).all()
    
    oneData = dict()
    oneData['state'] = oneState[0]

    subVenues = []
    for oneCity in stateCitys:
      aVenue = dict()
      aVenue['id'] = oneCity.id
      aVenue['name'] = oneCity.name
      aVenue['city'] = oneCity.city
      aVenue['num_upcoming_shows'] = 0
      subVenues.append(aVenue)
    
    oneData['venues'] = subVenues
    resultData.append(oneData)

  return render_template('pages/venues.html', areas=resultData)

#  ----------------------------------------------------------------  
#  Create: add a new venue - UI
#  ----------------------------------------------------------------
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

#  ----------------------------------------------------------------  
#  Create: add a new venue - Submit
#  ----------------------------------------------------------------
@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  form = request.form

  try:
    venu = Venue(name=form['name'], 
                  city=form['city'], 
                  state=form['state'],
                  address=form['address'],
                  phone=form['phone'])
 
    db.session.add(venu)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    flash( sys.exc_info())
  finally:
    db.session.close()

  if error == False:
    flash('Venue ' + form['name'] + ' was successfully listed!')
  
  return render_template('pages/home.html')

#  ----------------------------------------------------------------  
#  Search venues
#  ---------------------------------------------------------------- 
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  keyWords = request.form.get('search_term', '')
  likeWords = "%" + keyWords + "%"

  result = Venue.query.filter(Venue.name.ilike(likeWords) | 
                              Venue.city.ilike(likeWords) | 
                              Venue.state.ilike(likeWords)).order_by(Venue.name).all()

  viewItems = []
  if len(result) > 0:
    for oneResult in result:
      oneDic = dict()
      oneDic['id'] = oneResult.id
      oneDic['name'] = oneResult.name
      oneDic['num_upcoming_shows'] = 0
      viewItems.append(oneDic)

  response = {
    "count": len(result),
    "data": viewItems
  }

  return render_template('pages/search_venues.html', results=response, search_term=keyWords)

#  ----------------------------------------------------------------  
# Read: show details of a selected veneu
#  ---------------------------------------------------------------- 
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  venue = Venue.query.get(venue_id)
  if venue is None: 
    flash('Venue (with id: ' + str(venue_id) + ') not found')
    return redirect(url_for('venues'))

  past_shows, future_shows = getShowsWithVenueId(venue_id)

  data = dict()
  data['id'] = venue.id
  data['name'] = venue.name
  data['genres'] = stringToArray(venue.genres)
  data['address'] = venue.address
  data['city'] = venue.city
  data['state'] = venue.state
  data['phone'] = venue.phone
  data['image_link'] = venue.image_link
  data['facebook_link'] = venue.facebook_link
  data['upcoming_shows'] = future_shows
  data['upcoming_shows_count'] = len(future_shows)
  data['past_shows'] = past_shows
  data['past_shows_count'] = len(past_shows)

  return render_template('pages/show_venue.html', venue=data)

#  ----------------------------------------------------------------  
# Delete a venue
#  ----------------------------------------------------------------  
@app.route('/venues/<venue_id>/delete', methods=['POST'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error = False
  venue_name = ""

  try:
      venue = Venue.query.get(venue_id)
      venue_name = venue.name

      for show in venue.shows:
        venue.shows.remove(show)

      # Show table
      shows = Show.query.filter(Show.venue_id==venue_id)
      showIds = [oneShow.id for oneShow in shows]

      # clean Artist table
      for oneShow in shows:
        artist = Artist.query.get(oneShow.artist_id)
        for artistShow in artist.shows:
          if artistShow.id in showIds:
            artist.shows.remove(artistShow)

      # clean Show table
      shows.delete()
      
      # clean Venue table
      db.session.delete(venue)
      db.session.commit()
  except():
      db.session.rollback()
      error = True
  finally:
      db.session.close()

  if error:
    flash(sys.exc_info())
  else:
    flash('Venue ' + venue_name + 'deleted!')
  
  return render_template('pages/home.html')

#  ----------------------------------------------------------------  
#  Update: update details of a selected venue - UI
#  ----------------------------------------------------------------  
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  data = Venue.query.get(venue_id)

  venue = {
    "id": data.id,
    "name": data.name,
    "genres": stringToArray(data.genres),
    "city": data.city,
    "state": data.state,
    "phone": data.phone,
    "website": data.website,
    "facebook_link": data.facebook_link,
    "seeking_talent": data.seeking_talent,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": data.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

#  ----------------------------------------------------------------  
#  Update: update details of a selected venue - Submit
#  ----------------------------------------------------------------  
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form)
  error = False

  try:
    venue = Venue.query.get(venue_id)
    venue.name = form.name.data
    venue.phone = form.phone.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.genres = arrayToString(form.genres.data)
    venue.image_link = form.image_link.data
    venue.facebook_link = form.facebook_link.data
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    flash(sys.exc_info())
  finally:
    db.session.close()

  if error == True:
    flash('Failed to modify venue ' + form.name.data +'!')

  return redirect(url_for('show_venue', venue_id=venue_id))
