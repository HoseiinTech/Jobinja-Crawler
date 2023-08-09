import requests
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self):
        self.url = ('https://jobinja.ir/jobs?filters[keywords][]={keyword}&filters[locations][]={location}&filters['
                    'job_categories][]={category}')

    def get_box(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, features='html.parser')

        elements = [
            soup.find(class_='c-jobSearchTop__block c-jobSearchTop__block--list col-md-4 col-xs-12 u-block').find_all(name='option'),
            soup.find(class_='c-jobSearchTop__block col-md-4 col-xs-12 u-block').find_all(name='option')
        ]

        categories = []
        provinces = []

        for category in elements[0]:
            categories.append(category.get('value'))
        for province in elements[1]:
            provinces.append(province.get('value'))

        return [categories, provinces]

    def search(self, keyword, location='', category=''):
        response = requests.get(self.url.format(keyword=keyword,
                                                location=location,
                                                category=category))

        soup = BeautifulSoup(response.content, features='html.parser')
        elements = soup.find(id='jobSearchForm').find_all(
            name='div',
            class_='o-listView__itemWrap c-jobListView__itemWrap u-clearFix')

        jobs = []

        for item in elements:
            title = item.find(class_='c-jobListView__titleLink').text
            link = item.find(class_='o-listView__itemIndicator o-listView__itemIndicator--noPaddingBox')
            company = item.find(class_='c-jobListView__metaItem').text
            location = item.find_all(name='span')[2].text
            published_at = item.find(class_='c-jobListView__passedDays').text
            job = {
                'title': title.strip(),
                'link': link.get('href'),
                'company': company.strip(),
                'location': location.strip(),
                'published_at': published_at.strip()[1:-1]
            }
            jobs.append(job)

        return jobs


crawler = Crawler()

# Input

print('-----------WELCOME TO JOBINJA CRAWLER-----------')
keyword = input(' What job position are you looking for? ')
category = input(' Would you like me to search in a specific category? [N/y] => ')

box = crawler.get_box()

if category == 'y':
    print('\n------------------------------------------------\n')

    for category, i in zip(box[0][2:], range(len(box[0][2:]))):
        print(f'[{i}] {category}')

    print('\n------------------------------------------------\n')

    category_index = int(input(' Enter the category number: '))
    category = box[0][category_index+2]

    print('\n------------------------------------------------\n')
else:
    category = ''

province = input(' Do you want me to search in a specific province? [N/y] => ')

if province == 'y':
    print('\n------------------------------------------------\n')

    for province, i in zip(box[1][2:], range(len(box[1][2:]))):
        print(f'[{i}] {province}')

    print('\n------------------------------------------------\n')

    province_index = int(input(' Enter the province number: '))
    province = box[1][province_index+2]

    print('\n------------------------------------------------\n')
else:
    province = ''

for item in crawler.search(keyword, province, category):
    print(f"""
    
    Title: {item['title']}
    Company: {item['company']}
    Location: {item['location']}
    Published At {item['published_at']}
    
    Link: {item['link']}
    
    """)

print('------------------GOODBYE :)--------------------')