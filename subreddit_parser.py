# Get specified number of comments from subreddit

import praw
import psraw
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

userOrSubreddit = raw_input("Would you like to scrape a user or a subreddit? Type u for user, s for subreddit. \n")

# Ensure valid input
        
if (userOrSubreddit == "u"):
        user = raw_input("Which user's comments would you like to scrape?\n")

elif (userOrSubreddit == "s"):
        subreddit = raw_input("Which subreddit would you like to scrape?\n")
        
file = raw_input("What would you like to name your file? This is where you'll store all the data. Do not include the extension.\n")

fileName  = file + '.csv'

with open(fileName,'w') as f1:
	writer = csv.writer(f1, delimiter=',')
	index = 0

        # Scraping User
        if (userOrSubreddit == "u"):
                writer.writerow(["#","Comment","Timestamp(PT)", "Comment Score", "Number of Comments in Post", "Perpective Score"])
                for comment in reddit.redditor(user).comments.new(limit=20):
		        index += 1
		        print comment.body
		
		        perspectiveScore = runPerspective(comment.body)
			
		        row = [index,comment.body.encode('utf8'),datetime.datetime.fromtimestamp(int(comment.created_utc)).strftime('%Y-%m-%d %H:%M:%S').encode('utf8'), comment.score, comment.num_comments, perspectiveScore]

                        writer.writerow(row)

        # Scraping Subreddit
        elif (userOrSubreddit == "s"):

                maxNumComments = 5000
                
                # Initialize bookkeeping variables
                
                totalCommentCount = 0
                subCount = 0

                writer.writerow(["#", "Subreddit", "Submission", "Comment", "Timestamp(PT)", "Comment Score", "Number of Comments in Submission", "Perpective Score"])
                for submission in reddit.subreddit('politics').submissions():

                        if (totalCommentCount > maxNumComments):
                                break

                        subCount += 1
                        print("subCount: ")
                        print(subCount)
                        print("\n")

                        localCommentCount = 0

                        submission.comments.replace_more(limit=None)
                        
                        for comment in submission.comments.list():
                                totalCommentCount += 1
                                localCommentCount += 1

                                print("Total comment count: ")
                                print(totalCommentCount)
                                print("\n")

                                print("Local comment count: ")
                                print(localCommentCount)
                                print("\n")

                                print(submission.permalink)
                                print(comment.body)

		                perspectiveScore = runPerspective(comment.body)

                                # EACH ROW IN THE CSV CONTAINS:
                                # Subreddit name, submission link, index, comment body, timestamp, comment score, number of comments in submission,
                                # Google Perspective toxicity rating

                                row = [totalCommentCount, subreddit, submission.permalink, comment.body.encode('utf8'),datetime.datetime.fromtimestamp(int(comment.created_utc)).strftime('%Y-%m-%d %H:%M:%S').encode('utf8'), comment.score, submission.num_comments, perspectiveScore]

                                writer.writerow(row)
