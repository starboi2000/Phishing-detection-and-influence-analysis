# Phishing_detection-influence_analysis

<h2>What is this? and why this is relevant?</h2>
Phishing is a common tactic used by cybercriminals to steal personal and financial information from people. Phishing scams often take the form of an email or a bunch of text that influences people and pretends to be someone they are not, such as your bank or anything you will want to check in. It’s an important topic because, to be honest, the world is becoming more dangerous in the digital market every single day and millions of people are getting manipulated by these phishing activities and losing everything from their money to personal details. So, the basic approach is to make a web app where everything related to phishing will be there so a user can easily detect any mail, link or paragraph they are getting and can see whether it’s fake or real

<h2>How to run</h2>
* `git clone https://github.com/starboi2000/Phishing_detection-influence_analysis.git`
* `cd Full - App && mkdir contents`
* Download all the models and the topic_blacklist.txt from [drive](https://drive.google.com/drive/folders/1djyMa2-V-7HJfeHj17fdNeLvmmi0dE9K?usp=sharing)
* Put all the models and the files in that contents folder
* `pip install -r requirements.txt`
* Run `python app.py`


# detr-torch
Object Detection using Transformers

## Usage: 
* `git clone https://github.com/gittygupta/detr-torch.git`
* `cd detr-torch && mkdir saved_models`
* Download any of the models from [drive](https://drive.google.com/drive/folders/1XRVdKGgSOV-3DWli5yGcd51OUwJXDD8q?usp=sharing)
* Model Nomenclature: `detr_(Epoch Number).pth`
* Experimental results: `detr_4.pth` and `detr_6.pth` work best
* Save the model to the folder `saved_models`
* `python inference.py --model detr_{epoch_number}.pth --folder {path/to/images}`


