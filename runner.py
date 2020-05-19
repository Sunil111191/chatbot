import io
import random
import string
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
from flask import Flask, render_template, request
warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer
Response=str()

text_string=str()
Response="hhhh"
def my_bot(text_string):
    global Response
    f = open('E:/Tetrasoft/tetra_data/sample tetra data1 new.txt','r',errors = 'ignore')
    raw = f.read()
    raw = raw.lower()

    sent_tokens = nltk.sent_tokenize(raw) 
    word_tokens = nltk.word_tokenize(raw)


    lemmer = nltk.stem.WordNetLemmatizer()
    #WordNet is a semantically-oriented dictionary of English included in NLTK.
    def LemTokens(tokens):
        return [lemmer.lemmatize(token) for token in tokens]
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

    def LemNormalize(text):
        return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

    GREETING_INPUTS = ("hello", "hi", "greetings", "hi tetra", "what's up","hey",'namaste')
    GREETING_RESPONSES = ["hi", "hey", "hi buddy", "hi there", "hello", "I am glad! You are talking to me", 'namaste']
    def greeting(sentence):

        for word in sentence.split():
            if word.lower() in GREETING_INPUTS:
                return random.choice(GREETING_RESPONSES)



    def response(user_response):
        
        tetra_response=''
        sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx=vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if(req_tfidf==0):
            tetra_response=tetra_response+"Sorry! I don't understand you"
            return tetra_response
            Response=tetra_response
            
        else:
            tetra_response = tetra_response+sent_tokens[idx]
            return tetra_response
            Response=str(tetra_response)
            

    
    user_response = text_string
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            Response="tetra: You are welcome.."
        else:
            if(greeting(user_response)!=None):
                #print("tetra: "+greeting(user_response))
                Response=greeting(user_response)
            else:
                #print("tetra: ",end="")
                #print(response(user_response))
                Response=response(user_response)
                sent_tokens.remove(user_response)
    else:
        Response=str("tetra: Bye! take care..")
        
app = Flask(__name__, template_folder='templates',static_folder='static')

@app.route("/")
def index():
    return render_template("index1.html")
    #print(z)
    #return z
@app.route("/get")
#function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    my_bot(str(userText))
    return str(Response)

if __name__ == "__main__":
    app.run()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    