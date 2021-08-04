from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok
from validate_email import validate_email

# import ktrain
import pickle
import twint
import nest_asyncio
nest_asyncio.apply()
import urlexpander
import re

from bs4 import BeautifulSoup
import requests

import numpy as np
import tensorflow as tf
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def prep_data(text):
    tokens = tokenizer.encode_plus(text, max_length=512,
                                   truncation=True, padding='max_length',
                                   add_special_tokens=True, return_token_type_ids=False,
                                   return_tensors='tf')
    # tokenizer returns int32 tensors, we need to return float64, so we use tf.cast
    return {'input_ids': tf.cast(tokens['input_ids'], tf.float64),
            'attention_mask': tf.cast(tokens['attention_mask'], tf.float64)}

def scrape_user(username):
    print ("Fetching Tweets")
    c = twint.Config()
    c.Username = username # I used a different account for this project. Changed the username to protect the user's privacy.
    c.Pandas = True
    c.Limit = 2
    twint.run.Search(c)
    tweets = twint.storage.panda.Tweets_df
    return tweets[:20] # I have taken only 20 tweets for phishing detection

def site_info(sites):
    exp_sites = urlexpander.expand(sites)
    loaded_model = pickle.load(open('contents\\phishing.pkl', 'rb'))
    new_strings = []
    gform = []
    safe = []
    # word = 'https://www.'
    for i in exp_sites:
        # sites_1.append(i[8:])
        ht = requests.get(i).text
        soup = BeautifulSoup(ht, 'lxml')
        forms = soup.find('div', class_ = 'freebirdFormviewerViewFormContentWrapper')
        if (i[4]) == 's':
            safe.append(True)
        else:
            safe.append(False)
        new_strings.append(re.sub(r'https?:\/\/', '', i))
        if forms == None:
            gform.append(0)
        else:
            gform.append(1)
    if len(new_strings):
        result = loaded_model.predict(new_strings)
        for i in range(len(result)):
            if result[i] == 'Phishing ':
                if safe[i]:
                    result[i] = "Safe"
    else:
        result = ["No URLs found"]
        gform = ['']
        exp_sites = ['']
    
    return result, gform, exp_sites

app = Flask(__name__)
# run_with_ngrok(app)

action = "others"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def email_predict():
    mail = str(request.form.get('email'))
    is_valid = validate_email(email_address=mail, check_format=True, check_blacklist=True, check_dns=True, check_smtp=False, smtp_debug=False)
    # is_valid = validate_email(email_address=ins)

    # checker = validate_email(email_address=ins, check_format=True, check_blacklist=True, check_dns=True, check_smtp=False, smtp_debug=False)

    # if is_valid == True:
    #   if checker == True:
    #     print("This Email id exists and safe")
    #   else:
    #     print("This Email id exist but not safe")
    # else:
    #   print("This Email Id doesn't exist")

    if is_valid:
        result = 'Email id is safe'
    else:
        result = 'Email id is not safe'

    return render_template("index.html", mail_stat=result)

@app.route('/tweetcheck', methods=['POST'])
def tweets():
    tt = scrape_user(request.form.get("username"))
    tlist = []
    for i in range(len(tt)):
        tlist.append(tt['tweet'][i])

    link = []
    for i in tlist:
        link.append(re.findall(r'(https?://\S+)', i))
    mod_link = []
    for i in range(len(tlist)):
        if len(link[i]):
            mod_link.append(link[i])

    sites = []
    for i in mod_link:
        for j in i:
            sites.append(j)
    

    result, gform, exp_sites = site_info(sites)

    return render_template("tweetlinks.html", sites=exp_sites, site_stat=result, form=gform)

@app.route('/googleforms/<path:values>')
def form_check(values):
    
    html_text = requests.get(values).text
    soup = BeautifulSoup(html_text, 'lxml')
    forms = soup.find('div', class_ = 'freebirdFormviewerViewFormContentWrapper')
    entity_name = forms.find_all('div', class_ = 'm2' )
    # nn = entity_name['data-params'][5]
    result = []
    for j in range(len(entity_name)):
        i = 0
        nn = ''
        while(entity_name[j]['data-params'][i] != "\""):
            i += 1
        i += 1
        while(entity_name[j]['data-params'][i] != "\""):
            nn += entity_name[j]['data-params'][i]
            i += 1
        
        res_str = str(j+1) + '. ' + nn
        re_pattern = r'\b(?:cvv|password|account|pwd|a/c|expiration|otp|ifsc|debit|demat|pin|upi|atm)\b'
        safety = re.findall(re_pattern, nn.lower())
        if safety:
            res_str += " [Fobidden information]"
        else:
            res_str += " [Safe information]"
        result.append(res_str)
    return render_template("prediction.html", site_stat=result)

@app.route('/mailcheck', methods=['POST'])
def mail_check():
    mailtext = str(request.form.get('mail'))
    sites = re.findall(r'(https?://\S+)', mailtext)
    txt = re.sub(r'(https?://\S+)', '', mailtext)

    if txt == '':
        action = "sitecheck"
    elif sites == []:
        action = "textinfl"
    else:
        action = "mailcheck"

    return render_template("index.html", mail_sites=sites, mail_text=txt, prob=[], action=action)

@app.route('/sitecheck', methods=['POST'])
def site_check():
    mail_sites = request.form.get("mail1")
    sites = re.findall(r'(https?://\S+)', mail_sites)
    result, gform, exp_sites = site_info(sites)

    return render_template("tweetlinks.html", sites=exp_sites, site_stat=result, form=gform)

@app.route('/textinfl', methods=['POST'])
def textinfl():
    action = "textinfl"
    model = tf.keras.models.load_model('contents\\best_model')
    data = str(request.form.get('mail2'))
    prob = model.predict(prep_data(data))[0]
    # prob = model.predict(data, return_proba=True)
    infl = np.argmax(prob) + 1
    prob = [str(100*x)+'%' for x in prob]

    cialdini = {1:'Reciprocity', 2:'Scarcity', 3:'Authorization', 4:'Commitment', 5:'Liking', 6:'Concensus'}

    if infl != 7:
        
        infl = cialdini[infl]



    f = open("contents\\topic_blacklist.txt", 'r')
    words = f.read()
    words = words.split('\n')
    words = '|'.join(words)

    patt = r'\b(?:{})\b'.format(words)
    # sent = input("Enter you mail text: ")
    words = re.findall(patt, data[0].lower())

    # if len(words):
    #     print("Containing forbidden words like:")
    #     for word in words:
    #         print(word)
    # else:
    #     print("Not containing any forbidden words")
    
    return render_template("index.html", prob=prob, infl_val=infl, forbidden=words, action=action)

if __name__ == "__main__":
    app.run()
