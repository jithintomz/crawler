from bs4 import BeautifulSoup
import requests
import re
import itertools
import uuid
import urlparse

class Crawler():
    
    def __init__(self,seed_url):
        self.already_crawled = set([])
        self.seed_url = seed_url
        self.id = str(uuid.uuid4())

    def __crawl(self,url,depth):
        if depth!=0:
            self.already_crawled.update(url)
            child_list = []
            try:
                response = requests.get(url)
                soup_obj = BeautifulSoup(response.text, 'html.parser')
                child_list += [[url,urlparse.urljoin(url, x.get('src'))] for x in soup_obj.findAll('img') if x.get('src') is not None]
                for link in soup_obj.findAll('a', attrs={'href': re.compile("^http://")}):
                    child_url = link.get('href')
                    if child_url not in self.already_crawled:
                        child_list = itertools.chain(child_list,self.__crawl(child_url,depth-1))
            except requests.exceptions.ConnectionError:
                pass;
            for k in child_list:
                yield k        
        else:
            for m in iter(()):
                yield m


    def crawl(self,depth = None):
        self.already_crawled = set([])
        if depth == None:
            depth = 5
        result = self.__crawl(self.seed_url, depth)
        self.result = result
        return result


'''m = Crawler('https://sensehawk.com/')
final_list = m.crawl(depth = 5)

with open('test.txt', 'w') as handle:
    for item in final_list:
        handle.write("%s\n" % item)'''