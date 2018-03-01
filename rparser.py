import praw
import datetime
import csv
import json
import googleapiclient
from googleapiclient import discovery

def runPerspective(str):
	API_KEY='AIzaSyAlCwhKJ0C8n4eFM-ioPC5-MCFYy4P-TT8'

	# Generates API client object dynamically based on service name and version.
	service = discovery.build('commentanalyzer', 'v1alpha1', developerKey=API_KEY)

	analyze_request = {
		'comment': { 'text': str },
		'requestedAttributes': {'TOXICITY': {}}
	}
	try:
		response = service.comments().analyze(body=analyze_request).execute()
		json.dumps(response)
		return response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
		# print response.attributeScores.TOXICITY.summaryScore.value
	except googleapiclient.errors.HttpError as e:
		return "Error!"	

	

reddit = praw.Reddit(client_id='OlM6d2hKSrhbkw',
                     client_secret='w3kllzs-03WScaa9DFMHvRdTnQg',
                     password='WebW0rld',
                     user_agent='script by /u/sravyadivakarla123',
                     username='sravyadivakarla123')

print(reddit.user.me())

user = raw_input("What user's comments would you like to scrape?\n")
file = raw_input("What would you like to name your file? This is where you'll store all the data. Do not include the extension.\n")

#TESTING: default for testing 
#user = "shaggorama"
#fileName = "TEST"

fileName  = file + '.csv'


with open(fileName,'w') as f1:
	writer = csv.writer(f1, delimiter=',')
	writer.writerow(["#","Comment","Timestamp(PT)", "Comment Score", "Number of Comments in Post", "Perpective Score"])
	index = 0
	for comment in reddit.redditor(user).comments.new(limit=20):
		index += 1
		print comment.body
		
		perspectiveScore = runPerspective(comment.body)
			
		row = [index,comment.body.encode('utf8'),datetime.datetime.fromtimestamp(int(comment.created_utc)).strftime('%Y-%m-%d %H:%M:%S').encode('utf8'), comment.score, comment.num_comments, perspectiveScore]
		writer.writerow(row)

