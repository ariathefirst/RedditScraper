# ---------------- SUBREDDIT --------------------
# Get specified number of comments from subreddit
# -----------------------------------------------
import praw
import psraw
import sys
import datetime
import csv
import json
import googleapiclient
from googleapiclient import discovery
import codecs

# ----------------------------------------------------------
# Return Google Perspective score for a given string of text
# ----------------------------------------------------------
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
        # print response.attributeScores.TOXICITY.summaryScore.value
        return response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
	
    except googleapiclient.errors.HttpError as e:
        return "Error!"	

# ----------------------------------------------------------
#                          M A I N
# ----------------------------------------------------------

# Establish instance of reddit
reddit = praw.Reddit(client_id='OlM6d2hKSrhbkw',
                     client_secret='w3kllzs-03WScaa9DFMHvRdTnQg',
                     password='WebW0rld',
                     user_agent='script by /u/sravyadivakarla123',
                     username='sravyadivakarla123')

# Confirm successful instance initialization
# print(reddit.user.me())

# Take in CSV file of provided subreddits to scrape
# r --> read permissions only
csvFile = 'subreddit_list.csv'

all_subreddits = []

with open(csvFile, 'rU') as f:
    reader = csv.reader(f, delimiter=',')

    # Each item is a list of containing all items in the row
    for item in reader:
        all_subreddits.append(item[0])
        print(item[0])

fileName = 'subreddit_dump.csv'

# Add header
with open(fileName, 'a') as csv_:
    writer = csv.writer(csv_, delimiter=',')
    writer.writerow(["#", "Subreddit", "Submission", "Comment", "Timestamp(PT)", "Comment Score", "Number of Comments in Submission", "Perpective Score"])

# Traverse all subreddits and get comments from each one
# Append them all to subreddit_dump.csv

for subreddit in all_subreddits:    
    with open(fileName,'a') as f1:
        writer = csv.writer(f1, delimiter=',')
        index = 0

        maxNumComments = 1500
        
        # Initialize bookkeeping variables
        totalCommentCount = 0
        subCount = 0
        
        for submission in reddit.subreddit(subreddit).submissions():
            if (totalCommentCount > 1):
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

                row = [totalCommentCount, subreddit, submission.permalink, comment.body.encode('utf8'),
                           datetime.datetime.fromtimestamp(int(comment.created_utc)).strftime('%Y-%m-%d %H:%M:%S').encode('utf8'), comment.score,
                           submission.num_comments, perspectiveScore]

                writer.writerow(row)

