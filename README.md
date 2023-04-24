# Cloud Notification using Courier

## Objective
As more and more infrastructures are deployed in the cloud, there's a need to receive notification in case our cloud infrastructures experience some changes e.g. CPU utilization almost full, Virtual Machine changes status to Stopped, etc. While this notification feature is provided by Cloud Provider out of the box, we may need to subscribe the notification to various channels that we use individually. Also, message coming from cloud provider by default is not user-friendly and we need to convert it.

## Solution
Using [Courier](https://app.courier.com/), we can solve this issue. We can create notification template and integrate providers such as Email, SMS, and Slack in Courier, which then can be used by Cloud Provider serverless such as AWS Lambda or GCP Cloud Function to call and send notification to multi-channel. See Architecture below for more details.

## Architecture 
![courier cloud provider notification architecture](./screen-shot/Lambda%20Courier%20Architecture.png)

## Prerequisite
1. Python 3.9
2. AWS Account
3. Courier Account
4. Twilio Account
5. Slack Account
6. Gmail Account

## How to Setup
1. Follow Readme in this [link](https://github.com/shreythecray/secret-messages?utm_campaign=Developer%20Relations&utm_source=courier-hacks-open-source-devpost) to familiarize yourself with Courier and also to create accounts such as Gmail, Twilio, and Courier itself.
2. Follow this [link](https://www.courier.com/blog/automate-slack-and-microsoft-teams-notifications-using-python/) especially the part that shows how to create Slack App. Once done, please add a channel (I call mine `#cloud-notification`) in slack workspace and invite the bot to the channel. Take note of the `Channel ID` in `About` tab as it will be used in the lambda setup.
![slack bot in channel](./screen-shot/Slack%20Bot%20in%20Channel.png)
3. In the Courier app, go to Designer and then Create Template, name it anything you like, I use <b>Cloud Notification</b> as name. Configure 3 channels as per screen-shot below.
![Courier Email Template](./screen-shot/Courier%20Email%20Template.png)
![Courier SMS Template](./screen-shot/Courier%20SMS%20Template.png)
![Courier Slack Template](./screen-shot/Courier%20Slack%20Template.png)
Click the gear icon at the top (near the Cloud Notification in the screen shot) and take Notification ID which will be used during lambda setup.
4. Create your [AWS account](https://aws.amazon.com/).
5. [Create Standard SNS Topic](https://docs.aws.amazon.com/sns/latest/dg/sns-create-topic.html) in AWS account. Name it anything you like. My SNS topic in this tutorial is `dlm-notification`.
6. [Create event bridge rule](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule.html) that reacts to any AWS event you like. In this setup, I'll focus on EC2 Instance State Change. Below screen-shots are provided to help you setup and please follow exactly the JSON when configuring the transformer in Event Bridge as the exact attributes are required to make the lambda (python code) work.
![Event Bridge Rule Details](./screen-shot/Event%20Bridge%20Rule%20Details.png)
![Event Bridge Event Pattern 1](./screen-shot/Event%20Bridge%20Event%20Pattern%201.png)
![Event Bridge Event Pattern 2](./screen-shot/Event%20Bridge%20Event%20Pattern%202.png)
![Event Bridge Target](./screen-shot/Event%20Bridge%20Target.png)
![Event Bridge Transformer](./screen-shot/Event%20Bridge%20Transformer.png)
Full JSON for Template is below as the screen-shot can't display full value.

   `{
  "content": "EC2 Instance <instance> in account ID <account> and region <region> has changed state to <state>",
  "CloudProvider": "AWS",
  "Subject": "EC2 Instance State Change"
   }`

   Feel free to configure tags if you like and create rule in Review and update.
7. Prepare lambda package by following below instructions:
* In terminal, go to folder that contains this README file, then run `pip install --target ./package trycourier`
* Then, run `cd package/`
* Then, run `zip -r ../courier-lambda-package.zip .`
* Then, run `cd ..`
* Then, run `zip courier-lambda-package.zip index.py`
8. Create [AWS lambda](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html) that will host the python code. Below screen-shots and instructions are provided to help you setup the lambda.
![Lambda Creation Screen](./screen-shot/Lambda%20Creation%20Screen.png) Click Create Function at the bottom of the page, then upload the lambda package zip file created previously.
![Lambda Code Upload](./screen-shot/Lambda%20Code%20Upload.png)
In the Configuration -> Permissions tab, add permission to invoke lambda from SNS in Resource-based policy statements. Pls change the SNS topic Arn with the one you configure (don't use what is in the screen-shot).
![Lambda Configuration Permission](./screen-shot/Lambda%20Configuration%20Permission.png)
![Lambda Config Permission Policy Detail](./screen-shot/Lambda%20Config%20Permission%20Policy%20Detail.png)
Then, in Configuration -> Environment Variables, make sure you setup environment variables for below variables. Get the value from your Courier and Slack environment. For `DEST_EMAIL and DEST_PHONE`, put any email and phone you'd like to use to get notification from cloud event.

   `COURIER_TEMPLATE` is Courier Notification ID.

   `COURIER_TOKEN` is Courier API Key

   `SLACK_CHANNEL` is Slack Channel ID

   `SLACK_TOKEN` is Slack Bot OAuth Token
![Lambda Environment Variables](./screen-shot/Lambda%20Environment%20Variables.png)

## Testing
You can test the lambda by configuring test event or just creating EC2 instance and then changing the state of EC2. If it works, you'll see notification in your email, SMS, and slack channel.

See this video for demo.

## Next Step
1. Convert manual step mentioned in this README to using Terraform, AWS SAM, or Serverless framework.
2. Add another AWS event in Event Bridge but ensuring the Input Transformer will output JSON with content, CloudProvider, and Subject attributes.
3. Deploy the same function to another cloud provider e.g. GCP.