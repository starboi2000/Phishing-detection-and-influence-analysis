# Phishing_detection-influence_analysis

<h2>What is this? and why this is relevant?</h2>
Phishing is a common tactic used by cybercriminals to steal personal and financial information from people. Phishing scams often take the form of an email or a bunch of text that influences people and pretends to be someone they are not, such as your bank or anything you will want to check in. It’s an important topic because, to be honest, the world is becoming more dangerous in the digital market every single day and millions of people are getting manipulated by these phishing activities and losing everything from their money to personal details. So, the basic approach is to make a web app where everything related to phishing will be there so a user can easily detect any mail, link or paragraph they are getting and can see whether it’s fake or real


## How to run: 
* `git clone https://github.com/starboi2000/Phishing_detection-influence_analysis.git`
* `cd Full - App && mkdir contents`
* Download all the models and the topic_blacklist.txt from [drive](https://drive.google.com/drive/folders/1djyMa2-V-7HJfeHj17fdNeLvmmi0dE9K?usp=sharing)
* Put all the models and the files in that contents folder
* `pip install -r requirements.txt`
* Run `python app.py`


<p align="center">
    <img alt="Transformer" src="Screenshot (173).png" width=100%">
&nbsp; &nbsp; &nbsp; &nbsp;
</p>
                                                                 
<p>While running the app.py, you might incur a warning if you run it in a CPU in the above picture you can see it. If you have a GPU, then the processes in the app will be much faster. After running this app you will get "http://127.0.0.1:5000/" link where you can run the app on your browser </p>

## Our Result:
We have used urlexpander to expand the shortened urls(for our model to classify properly), validate_email to check whether the email id is safe or not, and also our influence detection model showed great prediction overall. And we have made our dataset using real-time advertisements and scraping twitter of different big companies. overall we got a satisfactory result in each cases.
<p>For evaluating the email id classifier we collected many email ids and it worked perfectly fine. Here’s one example with the real mail id of Flipkart</p>
<p align="center">
    <img alt="Transformer" src="Result/email 1.png" width=100%">
&nbsp; &nbsp; &nbsp; &nbsp;
</p>
<p>Now changing ‘k’ with ‘c’</p>
<p align="center">
    <img alt="Transformer" src="Result/email 2.png" width=100%">
&nbsp; &nbsp; &nbsp; &nbsp;
</p>
<p>Here we can see this model is giving the right prediction as the email id is not safe
<br/>
<p>After that Checked the Twitter model, it’s working fine for a given twitter id.
Example of this app is we can see in below, where I scraped my own twitter account and I have uploaded 2 Google form in my account, so we can see the results here how it can detect Google form also and if you click any link it’ll show the questions has been asked there and any question is asking forbidden information or not.</p>
 <p align="center">
    <img alt="Transformer" src="Result/twitter scrap.png" width=100%">
&nbsp; &nbsp; &nbsp; &nbsp;
</p>

<p>Fine-tune the Pre-Trained BERT model. Main focus was to check how a different learning rate changes the performance of a model for a particular dataset so keep the model same for both cases used different learning rate. Trained the model with learning rate 0.0001 and until 350 epochs, got the best accuracy at 349th number of 97.46% with the loss of 0.2252, saved the best one. you can see the accuracy and the loss below</p>
<p align="center">
    <img alt="Transformer" src="FULL DATA 2379/92.76(acc).png" width="45%">
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="EfficientDet" src="FULL DATA 2379/92.76(loss).png" width="45%">
</p>
