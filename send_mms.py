import libraries
import boto
import os
import uuid
import requests
import json
from boto.s3.key import Key

#S3 bucket and media file info
bucket_name = "<your_s3_bucket>"
bucket_region = "<your_s3_region>"
filepath = "/Users/username/<file_path>/<filename>.png"

#Flowroute MMS info
fromnum = "<your_flowroute_number>"
tonum = "<your_mobile_number>"
msg_body = "sample message"
#Import environment variables
AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
FR_ACCESS_KEY = os.environ['FR_ACCESS_KEY']
FR_SECRET_KEY = os.environ['FR_SECRET_KEY']

#Declare S3 connection to bucket
conn = boto.s3.connect_to_region(bucket_region,
               aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY
                             )
bucket = conn.get_bucket(bucket_name, validate=False)

#Generate random string
uid = uuid.uuid4()
hex32 = uid.hex

#Extract media file extension and recreate filename
filename = filepath.split('/')[-1]
fileext = filename.split('.')[-1]
upload_fn = hex32 + "." + fileext

#Upload file to S3 bucket
k = Key(bucket)
k.key = upload_fn
k.set_contents_from_filename(filepath, policy='public-read')

s3_url = "https://s3-" + bucket_region + ".amazonaws.com/" + bucket_name + "/" + upload_fn

#Send MMS
mmsdata = {"from": fromnum, "to": tonum, "body": msg_body, "media_urls":[s3_url], "is_mms": "true"}
fr_auth = (FR_ACCESS_KEY, FR_SECRET_KEY)
base = "https://api.flowroute.com/messages/v2.1"
headers = {"Content-Type": "application/vnd.api+json"}
r = requests.post(base, auth=fr_auth, json=mmsdata, headers=headers)
print r.status_code
