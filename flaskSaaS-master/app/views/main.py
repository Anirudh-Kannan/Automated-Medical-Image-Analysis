from flask import render_template, jsonify, Flask, redirect, url_for, request
from app import app
import random
import os
from flask.ext.login import login_user, logout_user, login_required, current_user
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import pandas as pd
import numpy as np
import os
import keras
import matplotlib.pyplot as plt
from keras.layers import Dense,GlobalAveragePooling2D, Conv2D, MaxPooling2D
from keras.applications import MobileNet
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.optimizers import Adam
import smtplib
from .user import *
from .emailclient import *
gmail_user = 'medisync.rvce@gmail.com'
gmail_password = 'medisync2020'

body = """\
Hey {}, 

Your results from MediSync's Chest X-ray Scan are ready. 

Our system predicts that there is a {}% chance that you have pneumonia.

Follow the information given on our website to learn more.

Take care.


Regards,

The MediSync Team
"""

email_text = """\
From: {}
To: {}
Subject: {}

{}
"""

def send_mail(to_email, to_name, prob):
    """
    to_email: email-id of receiver
    to_name: name of receiver
    prob: probability of pneumonia
    """
    subject = 'Results of MediSync Scan'

    text = body.format(to_name, int(prob))
    full_text = email_text.format(gmail_user, to_email, subject, text)
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to_email, full_text)
        server.close()
        print('Email sent!')
    except Exception as e:
        print(e)
    

if __name__ == '__main__':
    send_mail('dhruvbehl.cs17@rvce.edu.in', 'Dhruv', 0.3)

@app.route('/')

#disease_list = ['Atelectasis', 'Consolidation', 'Infiltration', 'Pneumothorax', 'Edema', 'Emphysema', \
                  # 'Fibrosis', 'Effusion', 'Pneumonia', 'Pleural_Thickening', 'Cardiomegaly', 'Nodule', 'Mass', \
                  # 'Hernia']

@app.route('/upload')
def upload_file2():
   return render_template('index.html')

def get_rez(pic):
    from keras.models import load_model
    new_model = load_model("/home/anirudh/Downloads/AI_Startup_Prototype-master/flaskSaaS-master/app/views/chest-xray-pneumonia.h5")
    img = image.load_img(pic, target_size=(224,224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    p_good,p_ill = np.around(new_model.predict(x), decimals=2)[0]
    return{'p_good':p_good,'p_ill':p_ill}
	
@app.route('/uploaded', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
        f = request.files['file']
        path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        dic = get_rez(path) 
        write_email('Anirudh','anirudhkannan2510@gmail.com',dic['p_ill']*100)
        f.save(path)
        return render_template('uploaded.html', title='Success', predictions=str(int(dic['p_ill']*100))+'%'
        , user_image=f.filename)


@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/map')
def map():
    return render_template('map.html', title='Map')


@app.route('/map/refresh', methods=['POST'])
def map_refresh():
    points = [(random.uniform(48.8434100, 48.8634100),
               random.uniform(2.3388000, 2.3588000))
              for _ in range(random.randint(2, 9))]
    return jsonify({'points': points})


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@app.route('/final_part')
def final_part():
    return render_template('final_part.html', title='More Information')