import sys, requests
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import csv
import dateutil.parser as dparser
import os
from collections import OrderedDict
def add_base_url(base_url, scheme, url):
    if url[-1]=='/':
        url=url[:-1]
    if urlparse(url).netloc=='':
        return scheme+"://"+base_url+url
    return url

def get_relevant_data(soup, website_name='Mangobaaz'):
    #currently just for www.mangobaaz.com
    is_valid_article = False
    if website_name=='Mangobaaz':
        try:
            data_dictionary=OrderedDict()

            heading_tag = soup.find('h1', {'class': 'md:text-3xl text-2xl leading-tight'})
            if heading_tag == None:
                return None
            date_tag = soup.find('div', {'class': 'text-sm font-bold uppercase my-2 tracking-1'}).text
            date_tag=date_tag.replace('By', '')
            date=dparser.parse(date_tag, fuzzy=True)
            author_name=date_tag[:date_tag.find('|')].replace('By','').strip()

            a = soup.findAll('p')
            article_text = ' '.join([paragraph.text for paragraph in a if paragraph.attrs=={}])

            data_dictionary['Date']=date
            data_dictionary['Author']=author_name
            data_dictionary['Headline']=heading_tag.text.replace(',',' ')
            data_dictionary['Article']=article_text.replace(',',' ')
            return data_dictionary
        except:
            return None


def Crawl_web(url, time_to_run=100):
    links = []
    url_scheme=urlparse(url)
    if url_scheme.scheme=='':
        print ("Please add http or https before requesting, thanks")
        return -1
    base_url=url_scheme.netloc
    main_url_list=[url]
    visited_list=[]
    counter=1
    dataset=[]
    end_time=time.time()+time_to_run
    i=0
    if os.path.exists(os.path.join(os.getcwd(),'main_url_list.txt')):
        print ("Getting data")
        f=open('main_url_list.txt','r')
        main_url_list=f.read().split('\n')
        f.close()
        f = open('visited_urls.txt', 'r')
        visited_list = f.read().split('\n')
        f.close()

    #while(i<5):
    while (time.time()<end_time) :
        i+=1
        temp_url_list=[]
        url_to_visit=main_url_list.pop(0)
        response=requests.request("GET",url_to_visit)
        #time.sleep(random.uniform(0.1,0.5))
        url_content=response.content

        soup = BeautifulSoup(url_content,'html.parser')
        data=get_relevant_data(soup, 'Mangobaaz')
        if data!=None:
            data['url']=url_to_visit.replace(',','')

            dataset.append(data)
            if len(dataset)%10==0:
                print ("Number of articles extracted"),
                print (str(len(dataset))+" Articles extracted\n")
                print("Number of visited urls and main urls: "),
                print(str(len(visited_list))+"  "+str(len(main_url_list)))
                print ('\n\n')
        visited_list.append(url_to_visit)
        temp_url_list2=[x.get('href') for x in soup.findAll('a')]
        temp_url_list2=[x for x in temp_url_list2 if urlparse(x).netloc=='' or urlparse(x).netloc==base_url and x!='/']
        temp_url_list2=[add_base_url(base_url,url_scheme.scheme, x) for x in temp_url_list2]
        main_url_list.extend(list(set(temp_url_list2).difference(set(visited_list))))

        main_url_list=list(set(main_url_list).difference(set(visited_list)))


    keys = dataset[0].keys()
    with open('Mangobaaz.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dataset)

    print ("len of visited list")
    f=open('visited_urls.txt','w')
    f.write('\n'.join(visited_list))
    f.close()
    f=open('main_url_list.txt','w')
    f.write('\n'.join(main_url_list))
    f.close()
    print (len(visited_list))
    print ("len of the mainurllist")
    print (len(main_url_list))
    return "Mangobaaz.csv"

