import os
import random
import sqlite3
import requests
import json
from googleapiclient.discovery import build

# insira seu token do Youtube API
api_key = ""

url = "http://127.0.0.1:5000/generate"

connection = sqlite3.connect('D:\Prog\PythonBack\src\database\database.sqlite')
cursor = connection.cursor()

youtube = build('youtube', 'v3', developerKey=api_key)


request = youtube.search().list(
    part='snippet',
    q='samples',
    maxResults=1,
    type='playlist'
)

plList = ["PLbx4KNApQrBlVMs8-GReVINZzWS6qg_xQ", "PL0bq757BcevzkBK1yAoElQWQ93Wp12iE_", "PLfNbP5vDLed9hnwMxuxWCq-2GfKdOGkO8", "PL878nmeXbewL04fhSU9oCD1p6DP8WY_oy"]
pl_request = youtube.playlistItems().list(
    part='snippet, contentDetails',
    # playlistId='PL6_dZKM8bf8f41K7JecDRKVyAij8KaBxd', # lewis one
    # playlistId='PLOIOSLQeUNaRu6oT4vHiIJDbHagbxXWJH', # no drums
    playlistId=random.choice(plList),
    
    maxResults=20
)


response = request.execute()

pl_request = pl_request.execute()

num = int('0')

vid_ids = []

for item in pl_request['items']:
    vid_ids.append(item['contentDetails'] ['videoId'])
    
vid_request = youtube.videos().list(
    part='snippet, contentDetails, statistics',
    id=','.join(vid_ids)
)

vid_response = vid_request.execute()

virNum = 0

print('These videos have less than 100k views')
try:
    for item in vid_response['items']:
        try:
            if int(item['statistics'] ['viewCount']) <= 100000:
                    
                print('Title: {0}'.format(item['snippet'] ['title']))
                print('Id: {0}'.format(item['id']))
                print('Description: {0}'.format(item['snippet'] ['description']))
                print('Views:{0}'.format(item['statistics'] ['viewCount']))
                print()

                myobj = { 
                            "title": "{0}".format(item['snippet'] ['title']), 
                            "idytb": "{0}".format(item['id']), 
                            "views": "{0}".format(item['statistics'] ['viewCount'])
                        }


                r = requests.post(url, json=myobj)

        except UnicodeEncodeError:
            print('There was an Unicode error, this video wont be registrated')
            pass
        except sqlite3.OperationalError:
            print('There was an SQLite3 error, this video wont be registrated')
            pass
except:
    print('There was an bigger error')


# myobj = { 
#             "title": "1", 
#             "idytb": "1", 
#             "views": "1" 
#         }

# c = json.dumps(myobj)
                    
# # text_file.write('} \n')

# # text_file.close()

# r = requests.post(url, json=myobj)

# payload = {'title': '1', 'idytb': '1', 'views': '1'}
# r = requests.get(url, params=payload)

# cursor.execute("SELECT * FROM savedsample")

# results = cursor.fetchall()

# print(results)
print(r)
