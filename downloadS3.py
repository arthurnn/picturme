import boto
import sys, os
from boto.s3.key import Key

LOCAL_PATH = '/home/vagrant/projects/picturme/'
AWS_ACCESS_KEY_ID = 'AKIAIC6VFIJCTGUNGU4A'
AWS_SECRET_ACCESS_KEY = '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'

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