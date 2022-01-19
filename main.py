import requests
import csv
import pandas as pd
import numpy
from bs4 import BeautifulSoup

url = "https://old.reddit.com/r/space/"

headers = {'User-Agent': 'Mozilla/5.0'}

req = requests.get(url, headers=headers)

soup = BeautifulSoup(req.text, 'html.parser')

domains = soup.find_all("span", class_="domain")

for domain in domains:
    if domain != "(self.space)":
        continue

    print(domain.text)

attrs = {'class': 'thing', 'data-domain': 'self.space'}

# GET DATA FOR 200 POST FROM SUBREDDIT r/space

counter = 1
while counter <= 200:
  for post in soup.find_all('div', attrs=attrs):
      title = post.find('p', class_="title").text
      
      try:
        author = post.find('a', class_='author').text
      except:
        author = '[deleted user]'
      
      likes = likes = post.find("div", attrs={"class": "score unvoted"}).text
      
      comments = post.find("a", class_="comments").text.split()[0]

      post_attrs = [counter, title, author, likes, comments]

      with open('output_text.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(post_attrs)

      counter += 1
  
  next_button = soup.find("span", class_="next-button")
  next_page_link = next_button.find("a").attrs['href']
  
  req = requests.get(url, headers=headers)
  soup = BeautifulSoup(req.text, 'html.parser')

# IMPORT CSV FILE AS PANDAS DATAFRAME

def import_csv(csv_name):
  data = pd.read_csv(csv_name)
  data.columns = ['counter', 'title', 'author', 'likes', 'comments']
  print(data.head())

final_data = import_csv("output_text.csv")

my_dict = {"Andromeda": 0,
        "Hubble": 0,
        "James Webb": 0,
        "Cassiopeia": 0,
        "Eclipse": 0,
        "Apollo": 0,
        "Sun": 0,
        "Moon": 0,
        "Mercury": 0,
        "Venus": 0,
        "Earth": 0,
        "Mars": 0,
        "Jupiter": 0,
        "Saturn": 0,
        "Uranus": 0,
        "Neptune": 0,
        "Pluto": 0}

titles = []

for title in data['title']:
  titles.append(title)

for key in my_dict.keys():
  for title in titles:
    if key in title:
      my_dict[key] += 1

print(my_dict)