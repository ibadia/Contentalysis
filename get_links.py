import sys, requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
def add_base_url(base_url, scheme, url):
    if url[-1]=='/':
        url=url[:-1]
    if urlparse(url).netloc=='':
        return scheme+"://"+base_url+url
    return url

def main(argv):
    ''' Main '''
    url=argv[1]

    links = []
    time_to_run=10 #run this script for 50 seconds and put all of the articles in the dump

    url_scheme=urlparse(url)
    if url_scheme.scheme=='':
        print ("Please add http or https before requesting, thanks")
        return -1

    base_url=url_scheme.netloc
    main_url_list=[url]
    visited_list=[]
    counter=1



    end_time=time.time()+time_to_run
    i=0
    while (i<2):
        i+=1
        temp_url_list=[]
        response=requests.request("GET",main_url_list.pop(0))
        soup = BeautifulSoup(response.content)
        visited_list.append(url)

        temp_url_list2=[x.get('href') for x in soup.findAll('a')]
        temp_url_list2=[x for x in temp_url_list2 if urlparse(x).netloc=='' or urlparse(x).netloc==base_url and x!='/']
        temp_url_list2=[add_base_url(base_url,url_scheme.scheme, x) for x in temp_url_list2]

        main_url_list.extend(list(temp_url_list2.difference(visited_list)))
        print (main_url_list)




        print (temp_url_list2)



if __name__ == "__main__":
    print('[*] Starting the main module')
    main(sys.argv)
