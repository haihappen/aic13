import feedparser
import time
from threading import Thread
from collections import deque
from HTMLParser import HTMLParser

class Task:
    def __init__(self, text):
        self.__text = text
    
    def get_text(self):
        return self.__text
    
    def get_keywords(self):
        return self.__keywords


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
                if "id" == a[0] and a[1] == "mediaarticlebody":
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


class Scraper(Thread):

    def __init__(self, tasks, link):
        Thread.__init__(self)
        self.__tasks = tasks
        self.__link = link
     
    def run(self):
        article = feedparser.parse(self.__link)
        parser = AicHTMLParser()
        parser.feed(article["feed"]["summary"])
        for p in parser.get_paragraphs():
            self.__tasks.append(Task(p))
            
        
def create_tasks():
    threads = []
    tasks = deque()
    rss = feedparser.parse("http://finance.yahoo.com/news/?format=rss")  # TODO: use more RSS links
    for entry in rss.entries:
        t = Scraper(tasks, entry["link"])
        t.start()
        threads.append(t)
        if len(threads) >= 5:
            for t in threads:
                t.join()
            threads = []
    for t in threads:
        t.join()
    return tasks


def main():
    tasks = create_tasks()
    for t in tasks:
        if t.get_text():
            print("task: " + t.get_text())

if __name__ == "__main__":
    start = time.time()
    main()
    print("time needed: %f" % (time.time() - start))
    
