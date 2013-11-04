from feedparser import parse
from time import time
from threading import Thread
from collections import deque
from HTMLParser import HTMLParser
from models import Paragraph
from datetime import datetime
from time import mktime
from django.utils.timezone import utc

class AicHTMLParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.__paragraphs = []
        self.__tmp = None
        self.__scrap = False
        self.__div = 0
        
    def handle_starttag(self, tag, attrs):
        if not self.__scrap:
            for a in attrs:
                if "id" == a[0] and (a[1] == "mediaarticlebody" or a[1] == "mediablogbody"):
                    self.__scrap = True
                    break  
        if self.__scrap:
            if tag == "div":
                self.__div += 1
            
            elif tag == "p":
                if self.__tmp != None:
                    raise Exception("TODO: paragraph inside paragraph")
                self.__tmp = str()
            
    def handle_data(self, data):
        if self.__tmp != None:
            self.__tmp += data
        
    def handle_endtag(self, tag):   
        if self.__scrap:
            if tag == "div":
                self.__div -= 1
                if self.__div == 0:
                    self.__scrap = False
            elif tag == "p":
                if self.__tmp != None and not self.__tmp.isspace():
                    self.__paragraphs.append(self.__tmp.strip())    
                self.__tmp = None
                
    def get_paragraphs(self):
        return self.__paragraphs


class Scraper:

    def __init__(self, tasks, link, published, yahoo_id):
        self.__tasks = tasks
        self.__link = link
        self.__published = datetime.fromtimestamp(mktime(published)).replace(tzinfo=utc)
        self.__yahoo_id = yahoo_id
     
    def run(self):
        article = parse(self.__link)
        parser = AicHTMLParser()
        parser.feed(article["feed"]["summary"])
        for p in parser.get_paragraphs():
            self.__tasks.append(Paragraph.objects.create(pub_date=self.__published, yahoo_id = self.__yahoo_id,text=p))
        if not self.__tasks:
            raise Exception("Could not scrap data from link: %s"%self.__link)
        
def scrap_yahoo():
    threads = []
    paragraphs = []
    rss = parse("http://finance.yahoo.com/news/?format=rss")  # TODO: use more RSS links
    for entry in rss.entries:
        yahoo_id = entry["id"]
        p = Paragraph.objects.filter(yahoo_id__exact=yahoo_id)
        if p:
            continue
        print("Scrap article from: %s" % entry["link"])
        t = Scraper(paragraphs, entry["link"], entry["published_parsed"],yahoo_id)
        t.run()
    return paragraphs

