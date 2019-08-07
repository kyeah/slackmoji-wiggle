import boto3
import time
import os
import sys
from slack import WebClient
from util import emojify

text1 = ":white_square: :white_square: :white_square: :white_square: :apple: :apple: :apple: :white_square: :white_square: :white_square: :white_square:\n:white_square: :white_square: :white_square: :apple: :apple: :apple: :apple: :apple: :apple: :white_square: :white_square:\n:white_square: :white_square: :white_square: :black_square: :black_square: :sunny: :sunny: :sunny: :white_square: :white_square: :white_square:\n:white_square: :white_square: :black_square: :sunny: :black_square: :sunny: :sunny: :black_square: :sunny: :sunny: :white_square:\n:white_square: :white_square: :white_square: :black_square: :sunny: :sunny: :sunny: :black_square: :black_square: :white_square: :white_square:\n:white_square: :white_square: :white_square: :white_square: :sunny: :sunny: :sunny: :sunny: :white_square: :white_square: :white_square:\n:white_square: :white_square: :apple: :apple: :blueberry: :apple: :apple: :apple: :apple: :white_square: :white_square:\n:white_square: :white_square: :apple: :apple: :blueberry: :blueberry: :blueberry: :apple: :apple: :apple: :white_square:\n:white_square: :white_square: :sunny: :sunny: :blueberry: :blueberry: :blueberry: :blueberry: :sunny: :sunny: :white_square:\n:white_square: :white_square: :sunny: :blueberry: :blueberry: :blueberry: :blueberry: :blueberry: :blueberry: :sunny: :white_square:\n:white_square: :white_square: :white_square: :blueberry: :blueberry: :white_square: :white_square: :blueberry: :blueberry: :white_square: :white_square:"

text2 = ":white_square: :white_square: :white_square: :white_square: :apple: :apple: :apple: :white_square: :white_square: :sunny: :sunny: \n:white_square: :white_square: :white_square: :apple: :apple: :apple: :apple: :apple: :apple: :sunny: :sunny: \n:white_square: :white_square: :white_square: :black_square: :black_square: :sunny: :sunny: :sunny: :white_square: :apple: :black_square: \n:white_square: :white_square: :black_square: :sunny: :black_square: :sunny: :sunny: :black_square: :sunny: :apple: :black_square: \n:white_square: :white_square: :white_square: :black_square: :sunny: :sunny: :sunny: :black_square: :black_square: :white_square: :white_square:\n:white_square: :white_square: :white_square: :white_square: :sunny: :sunny: :sunny: :sunny: :apple: :white_square: :white_square:\n:white_square: :white_square: :apple: :apple: :blueberry: :apple: :apple: :apple: :apple: :white_square: :white_square:\n:white_square: :sunny: :sunny: :apple: :blueberry: :blueberry: :blueberry: :apple: :apple: :bread: :white_square:\n:white_square: :sunny: :sunny: :apple: :blueberry: :blueberry: :blueberry: :blueberry: :bread: :bread: :white_square:\n:white_square: :white_square: :bread: :blueberry: :blueberry: :blueberry: :blueberry: :blueberry: :bread: :bread: :white_square:\n:white_square: :bread: :bread: :blueberry: :blueberry: :white_square: :white_square: :white_square: :white_square: :white_square: :white_square:"

slack_token = os.getenv("SLACK_TOKEN")

# =======================
# AWS & Credentials setup
#
if not slack_token:
    aws_ssm = boto3.client('ssm')
    aws_region = aws_ssm.meta.region_name

    resp = aws_ssm.get_parameter(
        Name=os.getenv('SLACK_TOKEN_SSM_SOURCE'),
        WithDecryption=True
    )

    slack_token = resp['Parameter']['Value']

slack = WebClient(slack_token)

channel = sys.argv[1]
#text1= emojify(sys.argv[2])
#text2= emojify(sys.argv[3])

res = slack.api_call('chat.postMessage', json={
    'channel': channel,
    'text': text1
})

params = {
    'ts': res['ts'],
    'channel': res['channel']
}

print('params:', params)

while True:
    # This will probably get you rate-limited.
    # 1 second intervals are safe but less FUN
    time.sleep(0.5)
    slack.api_call('chat.update', json={ **params, 'text': text2})
    time.sleep(0.5)
    slack.api_call('chat.update', json={ **params, 'text': text1})
