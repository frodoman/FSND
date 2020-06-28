from app import app, db, migrate, moment
from flask_sqlalchemy import SQLAlchemy
from datetime import *
from helper import *

#  ----------------------------------------------------------------  
#  Show table
#  ----------------------------------------------------------------  
class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))

  title = db.Column(db.String)
  description = db.Column(db.String)
  time = db.Column(db.DateTime)

  def __repr__(self):
    return f'<Venue {self.title} {self.time}>'

#  ----------------------------------------------------------------  
#  Reference table between Show and Artist, 
#  which is Many to Many relationship
#  ----------------------------------------------------------------  
show_artist = db.Table('show_artist', 
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
    db.Column('show_id', db.Integer, db.ForeignKey('Show.id'), primary_key=True)
)

#  ----------------------------------------------------------------  
#  Artist table
#  ----------------------------------------------------------------  
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    shows = db.relationship('Show', secondary=show_artist, 
            backref=db.backref('artists', lazy=True))

    def __repr__(self):
      return f'<Venue {self.id} {self.name} {self.city}>'
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#  ----------------------------------------------------------------  
#  Reference table between Show and Venue, 
#  which is Many to Many relationship
#  ----------------------------------------------------------------  
show_venue = db.Table('show_venue',
    db.Column('venu_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
    db.Column('show_id', db.Integer, db.ForeignKey('Show.id'), primary_key=True)
)

#  ----------------------------------------------------------------  
#  Venue table
#  ----------------------------------------------------------------  
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    website = db.Column(db.String(120))
    shows = db.relationship('Show', secondary=show_venue, 
            backref=db.backref('venues', lazy=True))
      
    def __repr__(self):
      return f'<Venue {self.id} {self.name} {self.city}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

#  ----------------------------------------------------------------  
#  Get all shows for a venue id
#  ----------------------------------------------------------------
def getShowsWithVenueId(venue_id):
  return getShowsWithId(venue_id, Venue())

#  ----------------------------------------------------------------  
#  Get all shows for an artist id
#  ----------------------------------------------------------------
def getShowsWithArtistId(artist_id):
  return getShowsWithId(artist_id, Artist())

#  ----------------------------------------------------------------  
#  Get all shows for a venue or artist id
#  ----------------------------------------------------------------
def getShowsWithId(itme_id, model:db.Model):

  if isinstance(model, Artist):
    shows = Show.query.filter(Show.artist_id == itme_id)
  else:
    shows = Show.query.filter(Show.venue_id == itme_id)
  
  now = datetime.now()
  future_shows = []
  past_shows = []

  if shows is not None:
    for one_show in shows:
      show_item = viewItemForAShow(one_show, model)
      if one_show.time > now: 
        future_shows.append(show_item)
      else:
        past_shows.append(show_item)
  
  return past_shows, future_shows

#  ----------------------------------------------------------------  
#  Convert a show object to displayable object
#  ----------------------------------------------------------------
def viewItemForAShow(show, model: db.Model):
  view_item = dict()
  view_item['start_time'] = dateTimeToString(show.time)

  if isinstance(model, Artist):
    view_item['venue_id'] = show.venue_id
    venue = Venue.query.get(show.venue_id)
    if venue is not None:
      view_item['venue_name'] = venue.name
      view_item['venue_image_link'] = venue.image_link
  else:
    view_item['artist_id'] = show.artist_id
    artist = Artist.query.get(show.artist_id)
    if artist is not None: 
      view_item['artist_name'] = artist.name
      view_item['artist_image_link'] = artist.image_link
  
  return view_item