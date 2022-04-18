from json import JSONDecodeError
from bs4 import BeautifulSoup
from string import punctuation
import requests
import os


def quote(url):
    link = requests.get(url, headers={'Accept-Language': 'en-Us,en;q=0.5'})
    if link:
        try:
            link = link.json()
            try:
                return print(link['content'])
            except KeyError:
                print('Invalid quote resource!')
        except JSONDecodeError:
            print('Invalid quote resource!')
    print('Invalid quote resource!')


def movie_seeker(url):
    needed_dict = {}
    response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if 'title' in url and 'imdb' in url:
        response = BeautifulSoup(response.content, 'html.parser')
        title = response.find('h1').text
        description = response.find('span', {'data-testid': 'plot-xl'}).text
        needed_dict["title"] = title
        needed_dict["description"] = description
        return print(needed_dict)
    else:
        print('Invalid movie page!')


def content(url):
    page_content = requests.get(url).content
    page_code = requests.get(url)
    if page_code:
        html = open('source.html', 'wb').write(page_content)
        if html:
            print('Content saved')
    else:
        print(f'The URL returned {page_code.status_code}')


def article(url, type_of, curr_folder):
    html_link = BeautifulSoup(requests.get(url).content, 'html.parser')
    articles = html_link.find_all('article')
    for article in articles:
        if article.find('span', {'data-test': 'article.type'}).text.strip('\n') == type_of:
            file_name = article.find('h3').text.strip('\n')
            file_name = file_name.replace(' ', '_')
            file_name = file_name.strip(punctuation)
            for i in range(len(file_name)):
                if file_name[i] in punctuation:
                    file_name = file_name.replace(file_name[i], '_')
            link_to_content = article.find('a', {'data-track-action': 'view article'})
            link_to_content = 'https://www.nature.com' + link_to_content.get('href')
            content_itself = BeautifulSoup(requests.get(link_to_content).content, 'html.parser')
            content_itself = content_itself.find('div', {'class': 'c-article-body'}).text.strip()
            content_itself = content_itself.encode()
            file = open(f'Page_{curr_folder}/{file_name}.txt', 'wb')
            file.write(content_itself)
            file.close()


number_of_pages = int(input())
needed_type = input()
for number in range(0, number_of_pages):
    os.mkdir(f'Page_{number + 1}')
    article(f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={number + 1}', needed_type, number + 1)
