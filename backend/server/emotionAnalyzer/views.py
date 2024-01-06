from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse

import json
import requests
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def preprocessText(text):
    cleaned_text=text.lower()
    cleaned_text=re.sub("@[A-Za-z0-9_]+"," ", cleaned_text)
    cleaned_text=re.sub("#[A-Za-z0-9_]+"," ", cleaned_text)
    cleaned_text=re.sub(r"http\S+", " ", cleaned_text)
    cleaned_text=re.sub(r"www.\S+", " ", cleaned_text)
    cleaned_text=re.sub('[()!?]', ' ', cleaned_text)
    cleaned_text=re.sub('\[.*?\]', ' ', cleaned_text)
    cleaned_text=re.sub("[^a-z0-9]"," ", cleaned_text)
    cleaned_text=re.sub('[0-9]+', " ", cleaned_text)
    cleaned_text=re.sub("rt","",cleaned_text)
    cleaned_text=cleaned_text.strip()
    return cleaned_text

def sentimentAnalysis(cleaned_text):
    score = SentimentIntensityAnalyzer().polarity_scores(cleaned_text)
    neg = score["neg"]
    neu = score["neu"]
    pos = score["pos"]
    com = score["compound"]
    print(f'Score : {com}')
    #Here the actual algorithm has to be replaced.  This is just a trial.
    if neg > 0:
        if com < -0.6:
            return (com, "Alarming!")
            # print(cleaned_text, "--------", "Alarming......!!!!")
        elif com < -0.5:
            return (com, "Level 3 : Consultation Needed")
            # print(cleaned_text, "--------", "Level 3 : Consultation needed")
        elif com < -0.4:
            return (com, "Level 2  : Some Help would be preferred")
            # print(cleaned_text, "--------", "Level 2  : some help would be preferred")
        elif com < -0.3:
            return (com, "Basic sadness")
    return (0, "You're Okay!")

        # print(cleaned_text, "--------", "Basic sadness")

@api_view(['POST'])
def getSadnessScore(request):
    if request.method == 'POST':
        text = request.data.get('text')
        cleaned_text = preprocessText(text)
        score, message = sentimentAnalysis(cleaned_text)
        if score or message:
           return JsonResponse({'score': score, 'message': message}, status=200)
        else:
           return JsonResponse({'error': f'An error occurred while computing Sadness Score'}, status=500)
        
@api_view(['POST'])
def getBulkSadnessScore(request):
    if request.method == 'POST':
        posts = request.data.get('posts')
        temp_posts=[]
        for post in posts:
            if(post['caption']):
                cleaned_text = preprocessText(post['caption'])
                score, message = sentimentAnalysis(cleaned_text)
                post['score'] = score
                post['message'] = message
            else:
                post['caption'] = 'No Caption Available'
                post['score'] = 0
                post['message'] = 'No Details Available'
        if score or message:
           return JsonResponse({'posts': posts}, status=200)
        else:
           return JsonResponse({'error': f'An error occurred while computing Sadness Score'}, status=500)

