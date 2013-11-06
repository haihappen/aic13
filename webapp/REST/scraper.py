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

    def __init__(self, tasks, entry):
        self.__tasks = tasks
        self.__link = entry["link"]
        self.__published = datetime.fromtimestamp(mktime(entry["published_parsed"])).replace(tzinfo=utc)
        self.__yahoo_id = entry["id"]
        self.__entry = entry
     
    def run(self):
        print("Scrape article: %s - %s" % (self.__entry["title"], self.__link))
        article = parse(self.__link)
        parser = AicHTMLParser()
        parser.feed(article["feed"]["summary"])
        for p in parser.get_paragraphs():
            self.__tasks.append(Paragraph.objects.create(pub_date=self.__published, yahoo_id=self.__yahoo_id, text=p))
        if not self.__tasks:
            raise Exception("Could not scrape data from link: %s" % self.__link)
        
def scrap_yahoo(latest):
    threads = []
    paragraphs = []
    rss = parse("http://finance.yahoo.com/news/?format=rss")  # TODO: use more RSS links
    
    for entry in rss.entries:
        if latest != None:
            if datetime.fromtimestamp(mktime(entry["published_parsed"])).replace(tzinfo=utc) > latest.pub_date:
                p = Paragraph.objects.filter(yahoo_id__exact=entry["id"])
                if p:
                    continue
                t = Scraper(paragraphs, entry)
                t.run()
        else:
            t = Scraper(paragraphs, entry)
            t.run()
            
    return paragraphs

def get_paragraphs(keyword, timestamp):
    if timestamp != None:
        paragraphs = Paragraph.objects.filter(text__contains=keyword, pub_date__gt=timestamp)
    else:
        paragraphs = Paragraph.objects.filter(text__contains=keyword) 
    return paragraphs
    
