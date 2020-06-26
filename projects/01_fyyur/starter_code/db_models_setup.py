from app import app, db, migrate, moment
from flask_sqlalchemy import SQLAlchemy

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

show_artist = db.Table('show_artist', 
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
    db.Column('show_id', db.Integer, db.ForeignKey('Show.id'), primary_key=True)
)

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

show_venue = db.Table('show_venue',
    db.Column('venu_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
    db.Column('show_id', db.Integer, db.ForeignKey('Show.id'), primary_key=True)
)

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