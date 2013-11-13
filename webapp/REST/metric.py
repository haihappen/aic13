from models import Answer
from models import Task
from models import SentimentAnalysis
from models import SentimentAnalysisType
from models import Company

class SimpleMetric():

    def __init__(self):
        self.__sentimentAnalysisTypeName = 'Simple'

        try:
            self.__sentimentAnalysisType = SentimentAnalysisType.objects.get(name = self.__sentimentAnalysisTypeName)
        except SentimentAnalysisType.DoesNotExist:
            self.__sentimentAnalysisType = SentimentAnalysisType.objects.create(name = self.__sentimentAnalysisTypeName)
        
    def calcMetric(self, company):
        print("Calculating sentiment for " + company.name)
        tasks = Task.objects.all().filter(company=company)

        sum = 0
        positives = 0
        for task in tasks:
            try:
                answer = Answer.objects.get(task=task)
                if answer.answer == 'neutral':
                    pass
                if answer.answer == 'positive':
                    sum += 1
                    positives += 1
                elif answer.answer == 'negative':
                    sum += 1
                else:
                    pass
            except Answer.DoesNotExist:
                pass
                
             
        if sum != 0:
            sentiment = int(float(positives)/float(sum)*100)
            print("Calculated sentiment: " + str(sentiment))
            try:
                sentimentAnalysis = SentimentAnalysis.objects.get(company = company)
                sentimentAnalysis.sentiment = sentiment
                sentimentAnalysis.save()
            except SentimentAnalysis.DoesNotExist:
                SentimentAnalysis.objects.create(company = company, type = self.__sentimentAnalysisType, sentiment = sentiment)
         

def calc_metric(answer):
    simpleMetric = SimpleMetric()
    task = Task.objects.get(id = answer["task"])
    company = task.company
    #company = Company.objects.get(id = task["company"])
    simpleMetric.calcMetric(company)
    
