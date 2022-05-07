from flask import Flask,render_template,request
from gnewsclient import gnewsclient
from newspaper import Article
from newspaper import Config
from datetime import datetime
import boto3
import nltk
import json
import wave

translate = boto3.client('translate')
polly = boto3.client('polly')
lastUpdate = 18
currentDate = datetime.now()
totalNews = {'English':{}, 'Hindi': {}}
speakText = ""
speakTextHindi = ""

app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/getNews')
def getNews():
    global totalNews
    global speakText
    global speakTextHindi
    global currentDate
    global lastUpdate
    if currentDate.hour>=lastUpdate and currentDate.hour<lastUpdate+3:
        return json.dumps(totalNews)
    else:
        print(lastUpdate)
        nltk.download('punkt')
        config = Config()
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        config.request_timeout = 10
        topics=['celebrity','sports','politician','business']
        news = {'celebrity':[], 'sports':[], 'politician':[], 'business':[]}
        hindiNews = {'celebrity':[], 'sports':[], 'politician':[], 'business':[]}
        for i in topics:
            try:
                client = gnewsclient.NewsClient(language='english',location='india',topic=i,max_results=3)
                news_list = client.get_news()
                if(len(news_list) < 3):
                    return getNews()
                for item in news_list:
                    article = Article(item['link'], language="en")
                    article.download()
                    article.parse()
                    article.nlp()
                    speakText = speakText + item['title'] + " " + article.summary + " "
                    news[i].append({'title': item['title'], 'summary':article.summary})
                    speakTextHindi = speakTextHindi + hindi_translate(item['title']) + " " + hindi_translate(article.summary) + " "
                    hindiNews[i].append({'title': hindi_translate(item['title']), 'summary':hindi_translate(article.summary)})
            except Exception as e:
                pass
        totalNews = {'English':news, 'Hindi': hindiNews}
        lastUpdate = lastUpdate + 3
        if lastUpdate==24:
            lastUpdate = 0
        SAMPLE_RATE = 16000
        CHANNELS = 1
        WAV_SAMPLE_WIDTH_BYTES = 2
        OUTPUT_FILE_IN_WAVE = 'static/englishSpeech.wav'
        FRAMES = []
        response=polly.synthesize_speech(Text=speakText[:1000],VoiceId='Aditi',OutputFormat='pcm',SampleRate=str(SAMPLE_RATE))
        stream = response.get("AudioStream")
        FRAMES.append(stream.read())
        WAVEFORMAT = wave.open(OUTPUT_FILE_IN_WAVE,'wb')
        WAVEFORMAT.setnchannels(CHANNELS)
        WAVEFORMAT.setsampwidth(WAV_SAMPLE_WIDTH_BYTES)
        WAVEFORMAT.setframerate(SAMPLE_RATE)
        WAVEFORMAT.writeframes(b''.join(FRAMES))
        WAVEFORMAT.close()
        OUTPUT_FILE_IN_WAVE = 'static/hindiSpeech.wav'
        FRAMES = []
        response2=polly.synthesize_speech(Text=speakTextHindi[:1000],VoiceId='Aditi',OutputFormat='pcm',SampleRate=str(SAMPLE_RATE))
        stream2 = response2.get("AudioStream")
        FRAMES.append(stream2.read())
        WAVEFORMAT2 = wave.open(OUTPUT_FILE_IN_WAVE,'wb')
        WAVEFORMAT2.setnchannels(CHANNELS)
        WAVEFORMAT2.setsampwidth(WAV_SAMPLE_WIDTH_BYTES)
        WAVEFORMAT2.setframerate(SAMPLE_RATE)
        WAVEFORMAT2.writeframes(b''.join(FRAMES))
        WAVEFORMAT2.close()
        return json.dumps(totalNews)
def hindi_translate(i):
    result=translate.translate_text(Text=i,SourceLanguageCode='en',TargetLanguageCode='hi')
    return result['TranslatedText']

if __name__=='__main__':
    app.run(host='localhost')
