from . import db
from sqlalchemy import asc, desc, func


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # name of the company
    website = db.Column(db.Text)  # website url to company
    twitter_handle = db.Column(db.String(50), unique=True)  # the twitter username
    twitter_followers = db.Column(db.Integer)  # the number of followers on twitter
    logo = db.Column(db.String(255))  # url to company image/logo
    rank = db.Column(db.Integer)
    fb_page_likes = db.Column(db.Integer)

    @staticmethod
    def top(num):
        return db.session.query(Company.name, Company.website, Company.logo,
                                (Company.fb_page_likes + Company.twitter_followers).label("rank")).order_by(desc(
            (Company.fb_page_likes + Company.twitter_followers))).limit(num)

    def __repr__(self):
        return "<Company '{}'>".format(self.name)
