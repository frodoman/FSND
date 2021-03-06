from app import *
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from forms import *
from db_models_setup import *

#  ----------------------------------------------------------------  
#  Show a list of artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.with_entities(Artist.id, Artist.name).order_by(Artist.name).all()

  return render_template('pages/artists.html', artists=artists)

#  ----------------------------------------------------------------  
#  Show details of a selected artist
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  artist = Artist.query.get(artist_id)
  if artist is None: 
    flash('Artist (with id: ' + str(artist_id) + ') not found')
    return redirect(url_for('venues'))

  past_shows, future_shows = getShowsWithArtistId(artist_id)

  data = dict()
  data['id'] = artist.id
  data['name'] = artist.name
  data['genres'] = stringToArray(artist.genres)
  data['image_link'] = artist.image_link
  data['city'] = artist.city
  data['state'] = artist.state
  data['phone'] = artist.phone
  data['facebook_link'] = artist.facebook_link
  data['upcoming_shows'] = future_shows
  data['upcoming_shows_count'] = len(future_shows)
  data['past_shows'] = past_shows
  data['past_shows_count'] = len(past_shows)

  return render_template('pages/show_artist.html', artist=data)

#  ----------------------------------------------------------------  
#  Update a selected artist - UI
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  data = Artist.query.get(artist_id)

  artist = {
    "id": data.id,
    "name": data.name,
    "genres": stringToArray(data.genres),
    "city": data.city,
    "state": data.state,
    "phone": data.phone,
    "website": data.website,
    "facebook_link": data.facebook_link,
    "seeking_venue": data.seeking_venue,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": data.image_link
  }

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

#  ----------------------------------------------------------------  
#  Update a selected artist - submit
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  form = ArtistForm(request.form)
  error = False

  try:
    artist = Artist.query.get(artist_id)
    artist.name = form.name.data
    artist.phone = form.phone.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.genres = arrayToString(form.genres.data)
    artist.image_link = form.image_link.data
    artist.facebook_link = form.facebook_link.data
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
    flash('Failed to modify artist ' + form.name.data +'!')

  return redirect(url_for('show_artist', artist_id=artist_id))

#  ----------------------------------------------------------------  
#  Create a new artist - UI
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

#  ----------------------------------------------------------------  
# Create a new artist - Submit
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  form = ArtistForm(request.form)
  flash('Genres ' + arrayToString(form.genres.data))

  try:
    artist = Artist(name=form.name.data, 
                    city=form.city.data, 
                    state=form.state.data,
                    phone=form.phone.data)
    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    flash(sys.exc_info())
  finally:
    db.session.close()

  if error == False and form.is_submitted():
    # on successful db insert, flash success
    flash('Artist ' + form.name.data + ' was successfully listed!')
  else:
    flash('Artist ' + form.name.data + ' failed to add!')

  return render_template('pages/home.html')

#  ----------------------------------------------------------------  
#  Search artists
#  ----------------------------------------------------------------
@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  keyWords = request.form.get('search_term', '')
  likeWords = "%" + keyWords + "%"

  result = Artist.query.filter(Artist.name.ilike(likeWords) | 
                               Artist.city.ilike(likeWords) | 
                               Artist.state.ilike(likeWords)).order_by(Artist.name).all()

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

  return render_template('pages/search_artists.html', results=response, search_term=keyWords)

#  ----------------------------------------------------------------  
#  Delete a selected artist - Submit
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/delete', methods=['POST'])
def delete_artist(artist_id):
  error = False
  artist_name = ""

  try:
      artist = Artist.query.get(artist_id)
      artist_name = artist.name

      for show in artist.shows:
        artist.shows.remove(show)

      # Show table
      shows = Show.query.filter(Show.artist_id==artist_id)
      showIds = [oneShow.id for oneShow in shows]

      # clean Venue table
      for oneShow in shows:
        venue = Venue.query.get(oneShow.venue_id)
        for venueShow in venue.shows:
          if venueShow.id in showIds:
            venue.shows.remove(venueShow)
      
      # clean Show table
      shows.delete()
      
      # clean Artist table
      db.session.delete(artist)
      db.session.commit()
  except():
      db.session.rollback()
      error = True
  finally:
      db.session.close()

  if error:
    flash(sys.exc_info())
  else:
    flash('Artist ' + artist_name + ' deleted!')
  
  return render_template('pages/home.html')