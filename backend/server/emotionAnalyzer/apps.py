from django.apps import AppConfig
import nltk

class EmotionanalyzerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emotionAnalyzer'

    # def ready(self):
    #     # Download vader_lexicon when the app is ready
    #     nltk.download('vader_lexicon')