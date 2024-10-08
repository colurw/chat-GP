import requests
from bs4 import BeautifulSoup
from time import sleep
from nltk.tokenize import PunktTokenizer
import pickle


medical_conditions = []

# get list of urls for common medical conditions on NHS website
request = requests.get('https://www.nhs.uk/conditions/')
soup = BeautifulSoup(request.content, 'html.parser')   
urls = [f"https://www.nhs.uk{url['href']}" for url in soup.find_all('a') if '/conditions/' in url['href'] and ' see ' not in url]
urls = [url for url in urls if url != 'https://www.nhs.uk/conditions/']
urls = [url for url in urls if '#' not in url]
urls = [url for url in urls if 'care-and-support-guide' not in url]

for url in urls:
    try:
        req = requests.get(url)
    except:
        print(url)   
        sleep(20) 
        req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    # detect extended pages
    child_urls = [f"https://www.nhs.uk{url['href']}" for url in soup.select('.nhsuk-contents-list__item a') if 'conditions' in url['href']]

    if child_urls:
        # scrape child pages and the overview
        child_urls.append(url)
        for url in child_urls:
            try:
                req = requests.get(url)
            except:
                print(url)
                sleep(20)
                req = requests.get(url)
            soup = BeautifulSoup(req.content, 'html.parser').find('article')
            text = soup.get_text(separator=' ', strip=True)
            output = text.split('. ')
            output = [sentence.replace(u'\xa0', ' ') for sentence in output]
            medical_conditions.append(output)
            sleep(0.5)
    else:
        # scrape short page
        text = soup.get_text(separator=' ', strip=True)
        output = text.split('. ')
        output = [sentence.replace(u'\xa0', ' ') for sentence in output]
        output.pop()
        medical_conditions.append(output)
        sleep(0.5)

with open('medical_conditions2.pickle', 'wb') as file:
    pickle.dump(medical_conditions, file, protocol=4)


common_medicines = []

# get list of urls for common medical conditions on NHS website
request = requests.get('https://www.nhs.uk/medicines/')
soup = BeautifulSoup(request.content, 'html.parser')   
urls = [f"https://www.nhs.uk{url['href']}" for url in soup.find_all('a') if '/medicines/' in url['href'] and ' see ' not in url]
urls = [url for url in urls if url != 'https://www.nhs.uk/medicines/']
urls = [url for url in urls if '#' not in url]

for url in urls:
    try:
        req = requests.get(url)
    except:
        print(url)   
        sleep(20) 
        req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    child_urls = [f"{url['href']}" for url in soup.select('.nhsuk-hub-key-links a') if 'medicines' in url['href']]

    for url in child_urls:
        try:
            req = requests.get(url)
        except:
            print(url)
            sleep(20)
            req = requests.get(url)

        soup = BeautifulSoup(req.content, 'html.parser').find('article')
        text = soup.get_text(separator=' ', strip=True)
        output = text.split('. ')
        output = [sentence.replace(u'\xa0', ' ') for sentence in output]
        common_medicines.append(output)
        sleep(0.5)

with open('common_medicines.pickle', 'wb') as file:
    pickle.dump(common_medicines, file, protocol=4)