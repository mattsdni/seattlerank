#! /usr/bin/env python

import json
import urllib

import csv
import tweepy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, prompt_bool
from sqlalchemy import MetaData, engine

from seattlerank import app, db
from seattlerank.models import Company

meta = MetaData()

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def insert_data():
    google = Company(name='Google', website='www.google.com', twitter_handle='google',
                     logo='http://www.thelogofactory.com/wp-content/uploads/2015/09/fixed-google-logo-font.png', rank=1)
    db.session.add(google)
    db.session.commit()

    print 'Initialized the database'


# This command updates the social media data for each company
@manager.command
def update_social():
    companies = Company.query.all()
    for company in companies:
        print company
    return


# This command will create all the companies for the first time and load their social media data too
@manager.command
def load_companies():
    with open('companies.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        data = []

        for row in spamreader:
            data.append(row)  # extract twitter user names
        data = data[1:]
    company_data = get_twitter_data(data)

    company_data_fb = get_facebook_data(data)

    # add fb data
    for company in company_data:
        try:
            company_data[company]['fb_likes'] = company_data_fb[company]
        except:
            print '-----ERROR----'
            print company + "doesn't have fb data, setting to 0"
            company_data[company]['fb_likes'] = 0

    for company in company_data:
        if company_data[company]['fb_likes'] > 0:
            print company_data[company]
        db.session.add(Company(name=company_data[company]['name'],
                               website=company_data[company]['website'],
                               twitter_handle=company_data[company]['twitter_handle'],
                               twitter_followers=company_data[company]['twitter_followers'],
                               logo=company_data[company]['logo'],
                               fb_page_likes=company_data[company]['fb_likes']))
    db.session.commit()

    print str(len(company_data)) + ' companies ranked'


def get_twitter_data(data):
    consumerKey = 'F3y4afxu50QoXcy4LYZRQzzG1'
    consumerSecret = 'tJhz8UyzRzl6oVzhQVLRC3kPI88zUxDmZi5EDrPaDrRLwmxTGK'
    accessToken = '4311911235-TTrMARu7MwR5pdcn6Q3WUoWe3AYl0cHByQo7vAt'
    accessSecret = '3rZyw2CnlcHNsGRD71yAl8YtseJc2mqAHcKvn6iLz0yeE'

    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessSecret)
    api = tweepy.API(auth)

    company_data = {}  # maps twitter handles to company data (name, website, etc...)
    for company in data:
        twitter_handle = company[2][1:] if (company[2][0] == '@') else company[2]
        company_data[twitter_handle] = {
            "name": company[0],
            "website": company[1],
            "twitter_handle": twitter_handle
        }

    chunks = [data[i:i + 99] for i in xrange(0, len(data), 99)]  # split into digestible chunks
    for chunk in chunks:
        # get just the usernames into a list
        usernames = []
        for company in chunk:
            usernames.append(company[2][1:] if (company[2][0] == '@') else company[2])

        users = api.lookup_users(screen_names=usernames)
        for i, user in enumerate(users):
            try:
                company_data[user.screen_name]["twitter_followers"] = user.followers_count
                company_data[user.screen_name]["logo"] = user.profile_image_url
            except:
                print '-------ERROR-------'
                print user.screen_name + 'does not exist'

    # if a company could not be found, set follower count to 0 and logo to ''
    for company in company_data:
        if 'twitter_followers' not in company_data[company]:
            company_data[company]['twitter_followers'] = 0
            company_data[company]['logo'] = ''

    return company_data


# returns a dict mapping twitter usernames to facebook page likes
def get_facebook_data(data):
    company_data = {}
    total = len(data)
    n = 1
    access_token = '1748920132064104%7C8Y31q_dkRE-io-TY9L_Q5Knii0Y'
    for company in data:
        print 'fetching ' + str(n) + ' of ' + str(total)
        n += 1

        url = "https://graph.facebook.com/v2.6/search?q=" + company[
            0] + "&type=page&access_token=" + access_token
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        company_id = data['data']
        if len(company_id) > 0:
            company_id = company_id[0]['id']
        else:
            continue

        url = "https://graph.facebook.com/v2.6/" + company_id + "/?fields=fan_count&access_token=" + access_token
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        try:
            twitter_handle = company[2][1:] if (company[2][0] == '@') else company[2]
            print twitter_handle
            company_data[twitter_handle] = data['fan_count']
        except:
            print company[0] + " doesn't have twitter or couldn't be found"

    return company_data


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to delete the whole database?"):
        db.drop_all()
        print 'Database deleted'


@manager.command
def erase_data():
    if prompt_bool("Are you sure you want to erase all data?"):
        for tbl in reversed(meta.sorted_tables):
            tbl.drop(engine)
        print 'Data erased'


if __name__ == '__main__':
    manager.run()
