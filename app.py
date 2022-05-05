from flask import Flask,render_template,request
from gnewsclient import gnewsclient
from newspaper import Article
from newspaper import Config
from datetime import datetime
import boto3
import nltk
import json
import pyaudio
from contextlib import closing

translate = boto3.client('translate')
polly = boto3.client('polly')
lastUpdate = 21
currentDate = datetime.now()
totalNews = {'English':{}, 'Hindi': {}}
speakText = ""
speakTextHindi = ""
stop = False

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
    if currentDate.hour>=lastUpdate and currentDate.hour<=lastUpdate+3:
        return json.dumps(totalNews)
    else:
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
        print(lastUpdate)
        return json.dumps(totalNews)
def hindi_translate(i):
    result=translate.translate_text(Text=i,SourceLanguageCode='en',TargetLanguageCode='hi')
    return result['TranslatedText']

@app.route('/speak')
def speak():
    global speakText
    global stop
    SAMPLE_RATE = 16000
    READ_CHUNK = 4096
    CHANNELS = 1
    BYTES_PER_SAMPLE = 2
    response=polly.synthesize_speech(Text=speakText[:1000],VoiceId='Aditi',OutputFormat='pcm',SampleRate=str(SAMPLE_RATE))
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(BYTES_PER_SAMPLE),channels=CHANNELS,rate=SAMPLE_RATE,output=True)
    with closing(response["AudioStream"]) as polly_stream:
        while True:
            data = polly_stream.read(READ_CHUNK)
            if data is None:
                break
            if stop:
                stop = False
                break
            stream.write(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return 'Success'

@app.route('/speakHindi')
def speakHindi():
    global speakTextHindi
    global stop
    SAMPLE_RATE = 16000
    READ_CHUNK = 4096
    CHANNELS = 1
    BYTES_PER_SAMPLE = 2
    response=polly.synthesize_speech(Text=speakTextHindi[:1000],VoiceId='Aditi',OutputFormat='pcm',SampleRate=str(SAMPLE_RATE))
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(BYTES_PER_SAMPLE),channels=CHANNELS,rate=SAMPLE_RATE,output=True)
    with closing(response["AudioStream"]) as polly_stream:
        while True:
            data = polly_stream.read(READ_CHUNK)
            if data is None:
                break
            if stop:
                stop = False
                break
            stream.write(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return 'Success'

@app.route('/stopSpeech')
def stopSpeech():
    global stop
    stop = True
    return 'Success'

if __name__=='__main__':
    app.run(host='localhost')
