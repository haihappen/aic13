import feedparser
import time
from threading import Thread
from collections import deque
from HTMLParser import HTMLParser

class Task:
    def __init__(self, keywords, text):
        self.__keywords = keywords
        self.__text = text
    
    def get_text(self):
        return self.__text
    
    def get_keywords(self):
        return self.__keywords


class AicHTMLParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.__paragraphs = []
        self.__current = []
        self.__tmp = None
        
    def handle_starttag(self, tag, attrs):
        if tag == "p":
            if self.__tmp != None:
                self.__current.append(self.__tmp)
            self.__tmp = str()
            
    def handle_data(self, data):
        if self.__tmp != None:
            self.__tmp += data
        
    def handle_endtag(self, tag):
        if tag == "p":
            self.__paragraphs.append(self.__tmp)
            if self.__current:
                self.__tmp = self.__current.pop()
            else:
                self.__tmp = None
                
    def get_paragraphs(self):
        return self.__paragraphs


class Scraper(Thread):

    def __init__(self, tasks, link, keywords):
        Thread.__init__(self)
        self.__tasks = tasks
        self.__link = link
        self.__keywords = keywords
     
    def run(self):
        article = feedparser.parse(self.__link)
        parser = AicHTMLParser()
        parser.feed(article["feed"]["summary"])
        for p in parser.get_paragraphs():
            for k in self.__keywords:
                if k in p:
                    self.__tasks.append(Task(self.__keywords, p))
                    break    
        
        
def create_tasks(keywords):
    threads = []
    tasks = deque()
    rss = feedparser.parse("http://finance.yahoo.com/news/?format=rss")  # TODO use more RSS links
    for entry in rss.entries:
        t = Scraper(tasks, entry["link"], keywords)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return tasks


def main():
    tasks = create_tasks(["Apple"])
    for t in tasks:
        print("task: " + t.get_text())

if __name__ == "__main__":
    start = time.time()
    main()
    print("running time: %f" % (time.time() - start))
    
