import json
from collections import Counter
from typing import Dict, List, Any
import re
from colorama import init, Fore, Style
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class TextAnalyzer:
   def __init__(self):
       init()
       try:
           nltk.download('vader_lexicon', quiet=True)
           nltk.download('punkt', quiet=True)
           nltk.download('stopwords', quiet=True)
       except Exception as e:
           print(f"Warning: Could not download NLTK data: {e}")
       
       self.sia = SentimentIntensityAnalyzer()
       self.stop_words = set(stopwords.words('english'))
       self.color_map = {
           'positive': 'positive',
           'negative': 'negative', 
           'neutral': 'neutral',
           'emphasis': 'emphasis',
           'question': 'question'
       }

   def load_messages(self, file_path: str) -> List[Dict[str, Any]]:
       """Load messages from JSON file"""
       try:
           with open(file_path, 'r', encoding='utf-8') as file:
               data = json.load(file)
               if not isinstance(data, dict) or 'messages' not in data:
                   raise ValueError("Invalid JSON format. Expected 'messages' key.")
               return data['messages']
       except Exception as e:
           print(f"Error loading file: {e}")
           return []

   def analyze_sentiment(self, text: str) -> Dict[str, float]:
       """Analyze sentiment of text"""
       return self.sia.polarity_scores(text)

   def color_code_text(self, text: str) -> str:
       """Add HTML color spans to text"""
       words = word_tokenize(text)
       colored_words = []
       
       for word in words:
           if word.lower() in self.stop_words:
               colored_words.append(word)
               continue
           
           sentiment = self.sia.polarity_scores(word)
           
           if sentiment['compound'] > 0.1:
               colored_words.append(f'<span class="{self.color_map["positive"]}">{word}</span>')
           elif sentiment['compound'] < -0.1:
               colored_words.append(f'<span class="{self.color_map["negative"]}">{word}</span>')
           elif word.endswith('?'):
               colored_words.append(f'<span class="{self.color_map["question"]}">{word}</span>')
           elif word.isupper():
               colored_words.append(f'<span class="{self.color_map["emphasis"]}">{word}</span>')
           else:
               colored_words.append(f'<span class="{self.color_map["neutral"]}">{word}</span>')
               
       return ' '.join(colored_words)

   def analyze_patterns(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
       """Analyze message patterns"""
       patterns = {
           'word_frequency': Counter(),
           'avg_message_length': 0,
           'question_count': 0,
           'emphasis_count': 0,
           'sentiment_trends': [],
           'unique_senders': set()
       }
       
       total_length = 0
       
       for message in messages:
           text = message.get('text', '')
           sender = message.get('sender', 'Unknown')
           words = word_tokenize(text.lower())
           patterns['word_frequency'].update(words)
           total_length += len(words)
           patterns['question_count'] += text.count('?')
           patterns['emphasis_count'] += len(re.findall(r'\b[A-Z]{2,}\b', text))
           patterns['sentiment_trends'].append(self.analyze_sentiment(text))
           patterns['unique_senders'].add(sender)
       
       if messages:
           patterns['avg_message_length'] = total_length / len(messages)
       
       return patterns