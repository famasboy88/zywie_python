# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

DIR = os.path.dirname(__file__)
cred = credentials.Certificate(os.path.join(DIR, 'service.json'))
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://zywie-2b7c2.firebaseio.com'
})
