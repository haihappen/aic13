from django.contrib import admin

from models import Company, SentimentAnalysisType, SentimentAnalysis, Paragraph, Task, Answer

admin.site.register(Company)
admin.site.register(SentimentAnalysisType)
admin.site.register(SentimentAnalysis)
admin.site.register(Paragraph)
admin.site.register(Task)
admin.site.register(Answer)
