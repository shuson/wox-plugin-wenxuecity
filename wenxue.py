# -*- coding: utf-8 -*-

import os
import shutil
import unicodedata
import webbrowser

import requests
from wox import Wox,WoxAPI
from bs4 import BeautifulSoup

URL = 'http://www.wenxuecity.com'

def full2half(uc):
    """Convert full-width characters to half-width characters.
    """
    return unicodedata.normalize('NFKC', uc)

class Main(Wox):
  
    def request(self,url):
        #break wall
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}

        #get system proxy if exists
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies = {
                "http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
                "https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))
            }
            return requests.get(url,proxies = proxies, headers=headers)
        
        return requests.get(url, headers=headers)
			
    def query(self, param):
        r = self.request(URL)
        bs = BeautifulSoup(r.content, 'html.parser')
        posts = bs.select('div.col ul li')
        result = []
        
        for p in posts[:30]:
            if not p.find('a') or p.find('a').get('class'):
                continue
            
            title = p.find('a').text
            link = URL + p.find("a")['href']
            
            item = {
                'Title': full2half(title),
                'SubTitle': u'enter to open',
                'IcoPath': os.path.join('img', 'wenxue.png'),
                'JsonRPCAction': {
                    'method': 'open_url',
                    'parameters': [link]
                }
            }
            result.append(item)
        
        return result
    
    def open_url(self, url):
        webbrowser.open(url) #use default browser

if __name__ == '__main__':
    Main()
