import requests
from bs4 import BeautifulSoup
from time import sleep
from nltk.tokenize import PunktTokenizer
import pickle


def request_html(url):
    try:
        req = requests.get(url)
    except:
        print(url)   
        sleep(30) 
        req = requests.get(url)
    return req


def paragraph_snipper(soup):
    """ inserts '_*SNIP*_' before heading strings to trigger split() when chunking """
    headings = soup.find_all('h2')
    for tag in headings:
        new_tag = soup.new_tag('h2')
        new_tag.string = f"_*SNIP*_{new_tag.text}"
        tag.replace_with(new_tag)

    subheadings = soup.find_all('h3')
    for tag in subheadings:
        new_tag = soup.new_tag('h3')
        new_tag.string = "_*SNIP*_"
        tag.replace_with(new_tag)

    return soup


def clean_corpus(corpus):
    """ removes sentences containing unwanted info"""
    output = []
    for chunk in corpus:
        sentences = chunk.split('. ')
        sentences = [sentence for sentence in sentences if 'http:' not in sentence and 'Credit:' not in sentence and 'Find out more' not in sentence and 'www:' not in sentence]
        sentences = [sentence for sentence in sentences if len(sentence) > 15]
        new_chunk = '. '.join(sentences).strip()
        if len(new_chunk) > 0:
            output.append(new_chunk)
    return(output)


medical_conditions = []
common_medicines = []


# # get list of urls for common medical conditions on NHS website
# request = requests.get('https://www.nhs.uk/conditions/')
# soup = BeautifulSoup(request.content, 'html.parser')   
# urls = [f"https://www.nhs.uk{url['href']}" for url in soup.find_all('a') if '/conditions/' in url['href'] and ' see ' not in url.text]
# urls = [url for url in urls if url != 'https://www.nhs.uk/conditions/']
# urls = [url for url in urls if '#' not in url]
# urls = [url for url in urls if 'care-and-support-guide' not in url]

# for url in urls:
#     req = request_html(url)
#     soup = BeautifulSoup(req.content, 'html.parser')

#     # detect extended pages
#     child_urls = [f"https://www.nhs.uk{url['href']}" for url in soup.select('.nhsuk-contents-list__item a') if 'conditions' in url['href']]

#     if child_urls:
#         # scrape child pages and the overview
#         child_urls.append(url)
#         for url in child_urls:
#             req = request_html(url)
#             soup = BeautifulSoup(req.content, 'html.parser')
#             soup = paragraph_snipper(soup)
#             soup = soup.find('article')
#             for section in soup.find_all('section'):
#                 text = section.get_text(separator=' ', strip=True)
#                 print(text)
#                 print()
#                 output = text.split('_*SNIP*_')
#                 output = [sentence.replace(u'\xa0', ' ') for sentence in output]
#                 medical_conditions.extend(output)   
#     else:
#         # scrape short page
#         soup = paragraph_snipper(soup)
#         soup = soup.find('article')
#         for section in soup.find_all('section'):
#             text = section.get_text(separator=' ', strip=True)
#             print(text)
#             print()
#             output = text.split('_*SNIP*_')
#             output = [sentence.replace(u'\xa0', ' ') for sentence in output]
#             medical_conditions.extend(output)

#     sleep(0.25)        

# medical_conditions = clean_corpus(medical_conditions)

# with open('medical_conditions3.pickle', 'wb') as file:
#     pickle.dump(medical_conditions, file, protocol=4)


# get list of urls for common medicines on NHS website
request = requests.get('https://www.nhs.uk/medicines/')
soup = BeautifulSoup(request.content, 'html.parser')   
urls = [f"https://www.nhs.uk{url['href']}" for url in soup.find_all('a') if '/medicines/' in url['href'] and ' see ' not in url.text]
urls = [url for url in urls if url != 'https://www.nhs.uk/medicines/']
urls = [url for url in urls if '#' not in url]

for url in urls:
    req = request_html(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    child_urls = [f"{url['href']}" for url in soup.select('.nhsuk-hub-key-links a') if 'medicines' in url['href']]

    for url in child_urls:
        req = request_html(url)
        soup = BeautifulSoup(req.content, 'html.parser')

        if 'common-questions-about' in url:
            soup = soup.find('article')
            for detail in soup.find_all('details'):
                text = detail.get_text(separator=' ', strip=True)
                print(text)
                print()
                output = [sentence.replace(u'\xa0', ' ') for sentence in output]
                common_medicines.extend(output)
        else:
            soup = paragraph_snipper(soup)
            soup = soup.find('article')
            for section in soup.find_all('section'):
                text = section.get_text(separator=' ', strip=True)
                print(text)
                print()
                output = text.split('_*SNIP*_')
                output = [sentence.replace(u'\xa0', ' ') for sentence in output]
                common_medicines.extend(output)
    sleep(0.25)

common_medicines = clean_corpus(common_medicines)

with open('common_medicines3.pickle', 'wb') as file:
    pickle.dump(common_medicines, file, protocol=4)