from app import *
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from forms import *
from db_models_setup import *
import helper
from datetime import *

#  ----------------------------------------------------------------  
#  Display all the up coming shows
#  ----------------------------------------------------------------
@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  presentShows = []
  now = datetime.now()
  shows = Show.query.filter(Show.time > now).order_by(Show.time).all()

  for oneShow in shows:
    data = {
      "venue_id": oneShow.venue_id,
      "venue_name": oneShow.venues[0].name,
      "artist_id": oneShow.artist_id,
      "artist_name": oneShow.artists[0].name,
      "artist_image_link": oneShow.artists[0].image_link,
      "start_time": dateTimeToString(oneShow.time)
    }
    presentShows.append(data)

  return render_template('pages/shows.html', shows=presentShows)

#  ----------------------------------------------------------------  
#  Create a new show -UI
#  ----------------------------------------------------------------
@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

#  ----------------------------------------------------------------  
#  Create a new show -Submit
#  ----------------------------------------------------------------
@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)
  flash(form.start_time.data)
  error = False

  artistId = form.artist_id.data
  venueId = form.venue_id.data

  try:
    show = Show()
    show.artist_id = artistId
    show.venue_id = venueId
    show.time = form.start_time.data

    #link to artist
    artist = Artist.query.get(artistId)
    artist.shows.append(show)
    
    #link to venu
    venue = Venue.query.get(venueId)
    venue.shows.append(show)
    
    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    flash(sys.exc_info())
  finally:
    db.session.close()

  # on successful db insert, flash success
  if error == True:
    flash('An error occurred. Show could not be listed.')
  else:
    flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')