import requests
from bs4 import BeautifulSoup
import csv


csvFile = open('logh.csv', 'w', newline = '')  #csvFile = open('log.xlsx', 'w', newline = '')
writer = csv.writer(csvFile) #writer = csv.writer(csvFile, dialect='excel')
writer.writerow(['url', 'title', 'text'])

def parse_details(link):
    html = requests.get(link)
    soup = BeautifulSoup(html.text, 'lxml')

    link.encode('utf-8').decode('utf-8', errors='ignore')
    print(link)

    title = soup.select_one('h1.title').text.strip()
    title.encode('utf-8').decode('utf-8', errors='ignore')
    print(title)

    text = soup.select_one('section#content p').text.strip()
    text.encode('utf-8').decode('utf-8', errors='ignore')
    print(text)
    try:
        writer.writerow([link, title, text])
    except UnicodeEncodeError:
        writer.writerow(['None', 'none', 'none'])

def parse():
    base_url = 'http://rl.odessa.ua/index.php'
    url = 'http://rl.odessa.ua/index.php/ru/poslednie-novosti?start=0'

    while True:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')

        for article in soup.select('article.item'):
            try:
                article_link = article.select_one('h1.title a')['href']
                #print(article_link)
                parse_details(base_url + article_link)
            except AttributeError as e:
                print(e)

        next_button = soup.find('a', class_='next', href=True)

        if next_button:
            url = base_url + next_button['href']
        else:
            break

parse()
csvFile.close()
