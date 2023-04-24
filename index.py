from trycourier import Courier
import os
import json

def lambda_handler(event, context):
  courier_token = os.environ['COURIER_TOKEN']
  slack_token = os.environ['SLACK_TOKEN']
  slack_channel = os.environ['SLACK_CHANNEL']
  courier_template = os.environ['COURIER_TEMPLATE']
  dest_email = os.environ['DEST_EMAIL']
  dest_phone = os.environ['DEST_PHONE']

  client = Courier(auth_token=courier_token)
  data = json.loads(event['Records'][0]['Sns']['Message'])

  message = {
    "to": {
      "slack": {
        "access_token": slack_token,
        "channel": slack_channel,
      },
      "email": dest_email,
      "phone_number": dest_phone,
    },
    "template": courier_template,
    "data": data,
    "routing": {
      "method": "all",
      "channels": ["sms", "email", "slack"]
    }
  }

  resp = client.send_message(
    message=message
  )
  print("Courier Request ID: ", resp['requestId'])
  return resp['requestId']