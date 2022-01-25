import requests
import csv
import pandas as pd
import numpy
from bs4 import BeautifulSoup

subreddit = input("Subreddit to search: ")
keyword = input("Keyword to count occurrences: ")

url = "https://old.reddit.com/r/" + subreddit + "/"

headers = {'User-Agent': 'Mozilla/5.0'}

req = requests.get(url, headers=headers)

soup = BeautifulSoup(req.text, 'html.parser')

domains = soup.find_all("span", class_="domain")

domain_type = "(self." + subreddit + ")"

for domain in domains:
    if domain != domain_type:
        continue

    print(domain.text)

data_domain = 'self.' + subreddit

attrs = {'class': 'thing', 'data-domain': data_domain}

# GET DATA FOR 500 POSTS FROM SUBREDDIT

counter = 1
while counter <= 500:
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

print(final_data['title'].head())

titles = []

occurrences = 0

for title in final_data['title']:
  titles.append(title)

for title in titles:
  if keyword in title:
    occurrences += 1

print("The word " + keyword + " appears " + str(occurrences) + " time(s) in the subreddit")