import praw
import datetime
import csv

reddit = praw.Reddit(client_id='OlM6d2hKSrhbkw',
                     client_secret='w3kllzs-03WScaa9DFMHvRdTnQg',
                     password='WebW0rld',
                     user_agent='script by /u/sravyadivakarla123',
                     username='sravyadivakarla123')

print(reddit.user.me())

user = raw_input("What user's comments would you like to scrape?\n")
fileName = raw_input("What would you like to name your file? This is where you'll store all the data. Do not include the extension.\n")

final_fname  = fileName + '.csv'


with open(final_fname,'w') as f1:
	writer = csv.writer(f1, delimiter=',')
	writer.writerow(["#","Comment","Timestamp(PT)", "Comment Score", "Number of Comments in Post"])
	index = 0
	for comment in reddit.redditor(user).comments.new(limit=1500):
		index += 1
		row = [index,comment.body.encode('utf8'),datetime.datetime.fromtimestamp(int(comment.created_utc)).strftime('%Y-%m-%d %H:%M:%S').encode('utf8'), comment.score, comment.num_comments]
		writer.writerow(row)

