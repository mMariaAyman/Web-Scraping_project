from bs4 import BeautifulSoup
import requests
from csv import writer
from itertools import zip_longest

url = "https://www.free-ebooks.net/web-design"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

href = soup.select('section div div div ul li a')
page_url = []
titles = []
prices = []
images = []
authors = []
discs = []

for h in href:
    page_url.append("https://www.free-ebooks.net" + h.attrs['href'])

page_url[0] = "https://www.free-ebooks.net/web-design"

for p in page_url:
    url = p
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    lists = soup.find_all('div', {'class': 'row laText'})
    for lis in lists:
        title = lis.find('a', {'class': 'title'}).text
        titles.append(title)
        author = lis.find('div', {'class': 'col-sm-12 padIt'}).text
        authors.append(author.replace('\n', ' '))
        price = lis.find('div', {'class': 'col-sm-12 hidden-xs padIt'})
        prices.append(price.text.replace('\n' and '\t', ''))
        image = lis.find('a', {'class': 'img'}).attrs['href']
        images.append('https://www.free-ebooks.net' + image)
        disc = lis.find('p', {'class': 'book-description'}).text
        discs.append(disc)

    with open('D:\pycharm\csv\Books.csv', 'w') as f:
        thewriter = writer(f)
        header = ['Book Title', 'Book Author', 'Book Description', 'Image URL']
        thewriter.writerow(header)
        info = [titles, authors, discs, images]
        thewriter.writerows(zip_longest(*info))

for i in range(len(images)):
    print("Image URL: {}\nBook Title: {}\nBook Author: {}\nBook Description: {}".format(images[i], titles[i],
                                                                                        authors[i], discs[i]))
