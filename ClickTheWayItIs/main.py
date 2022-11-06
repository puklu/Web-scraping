from bs4 import BeautifulSoup
import requests
import csv
from os.path import basename
from pathlib import Path

images_path = Path("images")
if not images_path.is_dir():  # if the images folder doesnt exist, create it
    images_path.mkdir(parents=True, exist_ok=True)

source = requests.get("https://clickthewayitis.blogspot.com/").text  # the request to get content from the URL

soup = BeautifulSoup(source, 'lxml')

# print(soup.prettify())

articles = soup.find_all('div', class_='post hentry uncustomized-post-template')  # all the posts on the page

# a csv to write the data to
csv_file = open('clickTheWayItIs.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Title', 'Poem', 'Link'])  # the header of the csv file

for article in articles:   # going through each post on the page
    title = article.find('h3', class_='post-title entry-title')   # title of the post
    poem = article.find('div', class_='post-body entry-content')  # the text of the post
    link = article.find('h3', class_='post-title entry-title')    # the link to the post

    img_src = article.find('img')['src']                          # link of the image of the post

    title = title.a.text                                          # extracting title text
    poem = poem.find_next().find_next_siblings()[1].text          # extracting text of the post
    link = link.a['href']                                         # extracting link of the post

    print(title)
    print(poem)
    print(link)
    print(img_src)
    print("----------------------")

    csv_writer.writerow([title, poem, link])             # writing the title, text and link of the post to the csv

    # saving the image in thr post in images directory
    with open(images_path / basename(img_src), "wb") as f:
        f.write(requests.get(img_src).content)

csv_file.close()
