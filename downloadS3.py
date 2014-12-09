import boto
import sys, os
from boto.s3.key import Key

LOCAL_PATH = '/home/vagrant/projects/picturme/'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', default=None)
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', default=None)

bucket_name = 'picturme_bucket'
# connect to the bucket
conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
                AWS_SECRET_ACCESS_KEY)
bucket = conn.get_bucket(bucket_name)
# go through the list of files
bucket_list = bucket.list('tiles')
for l in bucket_list:
  keyString = str(l.key)
  # check if file exists locally, if not: download it
  if not os.path.exists(LOCAL_PATH+keyString):
    l.get_contents_to_filename(LOCAL_PATH+keyString)
