#!/usr/bin/env python
import copy
import json
import math
import os
import random
import time

from pprint import pprint

import boto
import boto.sqs

from fluent import event
from fluent import sender

from pymongo import MongoClient

#SQS
region = os.getenv('REGION', default='us-east-1')
queue_name = os.getenv('SQS_NAME')

# Fluentd
fluentd_topic = os.getenv('FLUENTD_TOPIC', default='test')
fluentd_host = os.getenv('FLUENTD_HOST', default='127.0.0.1')
fluentd_port = int(os.getenv('FLUENTD_PORT', default=24224))

if __name__=="__main__":
	conn = boto.sqs.connect_to_region(region)
	#fluentd logger
	sender.setup(fluentd_topic, host=fluentd_host, port=fluentd_port)
	email_sqs = conn.get_queue(str(queue_name))
	result = email_sqs.get_messages(10)
	while len(result) > 0:
		for message in result:
			data = json.loads(message.get_body())
			# process the message
			if 'bounce' in data:
				if 'diagnosticCode' in data['bounce']['bouncedRecipients'][0]:
					msgCode = data['bounce']['bouncedRecipients'][0]['diagnosticCode']
				else:
					msgCode = ""
				sendData = {
					'emailAddress': data['bounce']['bouncedRecipients'][0]['emailAddress'],
					'bounceType': data['bounce']['bounceType'],
					'bounceSubType': data['bounce']['bounceSubType'],
					'diagnosticCode': msgCode,
					'timestamp': data['bounce']['timestamp']
				}
				pprint (sendData)
				event.Event('email', sendData)
				email_sqs.delete_message(message)
				pass
			pass
		result = email_sqs.get_messages(10)
		pass
	print "There is no more msg in the queue"

