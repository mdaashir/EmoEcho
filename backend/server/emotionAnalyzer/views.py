from rest_framework import viewsets
from rest_framework.decorators import action
from django.http import JsonResponse
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def preprocessText(text):
    cleaned_text = text.lower()
    cleaned_text = re.sub("@[A-Za-z0-9_]+", " ", cleaned_text)
    cleaned_text = re.sub("#[A-Za-z0-9_]+", " ", cleaned_text)
    cleaned_text = re.sub(r"http\S+", " ", cleaned_text)
    cleaned_text = re.sub(r"www.\S+", " ", cleaned_text)
    cleaned_text = re.sub('[()!?]', ' ', cleaned_text)
    cleaned_text = re.sub('\[.*?\]', ' ', cleaned_text)
    cleaned_text = re.sub("[^a-z0-9]", " ", cleaned_text)
    cleaned_text = re.sub('[0-9]+', " ", cleaned_text)
    cleaned_text = re.sub("rt", "", cleaned_text)
    cleaned_text = cleaned_text.strip()
    return cleaned_text

def sentimentAnalysis(cleaned_text):
    score = SentimentIntensityAnalyzer().polarity_scores(cleaned_text)
    neg = score["neg"]
    neu = score["neu"]
    pos = score["pos"]
    com = score["compound"]
    print(f'Score : {com}')
    if neg > 0:
        if com < -0.6:
            return (com, "Alarming!")
        elif com < -0.5:
            return (com, "Level 3 : Consultation Needed")
        elif com < -0.4:
            return (com, "Level 2 : Some Help would be preferred")
        elif com < -0.3:
            return (com, "Basic sadness")
    return (0, "You're Okay!")

class EmotionAnalyzer(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def get_sadness_score(self, request):
        text = request.data.get('text')
        cleaned_text = preprocessText(text)
        score, message = sentimentAnalysis(cleaned_text)
        if score or message:
            return JsonResponse({'score': score, 'message': message}, status=200)
        else:
            return JsonResponse({'error': 'An error occurred while computing Sadness Score'}, status=500)

    @action(detail=False, methods=['post'])
    def get_bulk_sadness_score(self, request):
        posts = request.data.get('posts')
        for post in posts:
            if post['caption']:
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
            return JsonResponse({'error': 'An error occurred while computing Sadness Score'}, status=500)