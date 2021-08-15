import requests
import os
import pdb

API_KEY = os.environ['NASA_KEY']

url = 'https://api.nasa.gov/neo/rest/v1/feed'

payload = {'start_date': '2021-05-01', 'end_date': '2021-05-02', 'API_KEY': API_KEY}

res = requests.get(url, params=payload)

res.url

data = res.json()
pdb.set_trace()

print(data)
# for date in data['near_earth_objects']: #the keys for data['near_earth_objects] are the dates from start to end
#     print(date)
#     print()
#     print()
#     for line in data['near_earth_objects'][date]: #value 
#         print(line)
#         print()
#         print()
#         print()
#         print()
#         print()

# print(data)
