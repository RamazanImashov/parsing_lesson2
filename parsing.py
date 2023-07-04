import requests
import lxml
from bs4 import BeautifulSoup
import csv

def get_html(url):
    response = requests.get(url)
    return response.text

def write_to_csv(data):
    with open('data.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([data['title'], data['price'], data['desc'], data['mileage'], data['image']])
    
def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    page_list = soup.find('div', class_="pages fl").find_all('a')[-1].text
    return page_list
    print(page_list)


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    cars_list = soup.find('div', class_ = "catalog-list").find_all('a')
    
    
    for car in cars_list[:20]:
        try:
            title = car.find('span', class_ = "catalog-item-caption").text.strip()
        except AttributeError:
            title = ''
        # print(title)
        try:
            price = car.find('span', class_ = "catalog-item-price").text.strip()
        except AttributeError:
            price = ''
        # print(price)
        try:
            image = car.find('img', class_ = "catalog-item-cover-img").get('src')
        except AttributeError:
            image = ''
        # print(image)
        try:
            mileage = car.find('span', class_ = "catalog-item-mileage").text
        except AttributeError:
            mileage = ''
        # print(mileage)
        try:
            desc = car.find('span', class_ = "catalog-item-descr").text.split()
            desc = ' '.join(desc)
        except AttributeError:
            desc = ''
        # print(desc)
        data = {
            'title': title,
            'price': price,
            'image': image,
            'mileage': mileage,
            'desc': desc
        }
        write_to_csv(data)

def main():
    url = 'https://cars.kg/offers'
    page = 1
    while True:  
        gep_url = url + '/' + str(page)
        html = get_html(gep_url)
        get_data(html)
        if get_total_pages(get_html(gep_url)) == 'Далее ⇢':
            page += 1
        else:
            break
            


    
with open('data.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['title', 'price', 'desc', 'mileage', 'image'])
        
main()

