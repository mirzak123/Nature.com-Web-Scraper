import string
import requests
import os

from bs4 import BeautifulSoup


"""
STAGE 2:

from bs4 import BeautifulSoup


print("Input the URL:")
url = input()
response = requests.get(url, headers={'Accept-Language': 'en-US, en;q=0.5'})

if response.status_code == 200 and 'imdb.com/title' in url:
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1').text
    description = soup.find('span', {'data-testid': 'plot-l'}).text
    movie_content = {'title': title, 'description': description}
    print(movie_content)
else:
    print("Invalid movie page!")
---------------------------------------------------------------------------
STAGE 3:
print("Input the URL:")
url = input()
response = requests.get(url)

if response.status_code == 200:
    page_content = response.content
    print(type(page_content))
    with open('source.html', 'wb') as movie_source_file:
        movie_source_file.write(page_content)
        # print(page_content, file=movie_source_file)
        print("Content saved.")
else:
    print(f"The URL returned {response.status_code}")
"""


def format_title_names(titles):
    punctuation = string.punctuation + '—'
    for i, title in enumerate(titles):
        title = title.translate(str.maketrans('', '', punctuation))
        title = title.split()
        title = '_'.join(title)
        titles[i] = title


# go through articles in one page one by one
def loop_through_articles(raw_articles, selected_article_type):
    titles = []
    article_links = []

    for raw_article in raw_articles:
        article_type = raw_article.find('span', "c-meta__type").text
        if article_type == selected_article_type:
            title_raw = raw_article.find('h3', {"itemprop": "name headline"})
            body_raw = raw_article.find('a', {"class": "c-card__link u-link-inherit"})

            titles.append(title_raw.text.strip())
            article_links.append(body_raw.get('href'))

    # title formatting removes punctuation and replaces whitespaces with an underscore: '_'
    format_title_names(titles)

    for title, article_link in zip(titles, article_links):
        print(title, article_link)
        print()
        article_body = get_article_content(article_link)
        write_article_to_file(title, article_body)


def write_article_to_file(title, article_body):
    with open(title + '.txt', 'w', encoding='utf-8') as news_file:
        news_file.write(article_body)


def get_article_content(article_link):
    article_page = requests.get('https://www.nature.com' + article_link)
    soup = BeautifulSoup(article_page.content, 'html.parser')

    article_body = soup.find('div', attrs={"class": "c-article-body"})

    if article_body:
        article_body = article_body.text.strip()
    else:
        article_body = ''
    return article_body


def scrape_current_page(page_num, article_type):
    url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=' + str(page_num)
    response = requests.get(url, headers={'Accept-Language': 'en-US, en;q=0.5'})
    soup = BeautifulSoup(response.content, 'html.parser')

    articles_raw = soup.find_all('article')

    loop_through_articles(articles_raw, article_type)


def main():
    number_of_pages = int(input("Enter number of pages you want to look through: "))
    article_type = input("Enter the Article Type you're looking for: ")
    # print(os.getcwd())
    print(f"\nSearching for articles of type {article_type}:")
    # will go through the entered number of pages and make a directore Page_N for each one
    for page in range(1, number_of_pages + 1):
        os.mkdir('Page_' + str(page))
        os.chdir('Page_' + str(page))

        scrape_current_page(page, article_type)

        os.chdir(r'C:\Users\user\PycharmProjects\Web Scraper\Web Scraper\task')
    print("Saved all found articles!")


if __name__ == "__main__":
    main()
