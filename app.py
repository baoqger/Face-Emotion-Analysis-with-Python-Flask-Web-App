import json
import os
from flask import Flask, render_template, request
import indicoio
from werkzeug import secure_filename
from flask import send_from_directory

# lib needed for the image analysis
from PIL import Image
import numpy as np
import indicoio


UPLOAD_FOLDER = './uploads/'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])




app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    '''Shows index page at localhost:5000'''
    return render_template('index_v3.html')


@app.route('/crunch', methods=['POST'])
def send_to_indico():
    '''
    This route handles the server's response when
    you post data to localhost:5000/crunch through
    the form on index.html
    '''

    tweets_csv_string = request.form.get('tweets')
    csv_list = tweets_csv_string.replace('\r', '').splitlines()

    if len(csv_list) > 40:
        csv_list = csv_list[:40]
    print csv_list
    tweet_list = []
    for csv_tweet in csv_list:
        tweet_only = csv_tweet.split(',')[2:]
        tweet_list.append(','.join(tweet_only))

    tweet_list = tweet_list[::-1]

    #tweet_scores = indicoio.batch_sentiment(tweet_list, api_key="428b1c1039ed8d8eaa886ee88044debd")
    tweet_scores = indicoio.sentiment_hq(tweet_list, api_key="428b1c1039ed8d8eaa886ee88044debd")
    return json.dumps({'scores': tweet_scores, 'tweets': tweet_list})  # dumps converts res to a JSON object


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        #print "post method"
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('uploaded_file',filename=filename))
            result = image_analysis(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print type(result)
            return json.dumps({'sentiment':result.keys(),'score':result.values()})
            #return json.dumps({'aftervalue':"baoqger"})



#analyse the uploaded image
def image_analysis(filepath):
	indicoio.config.api_key = '428b1c1039ed8d8eaa886ee88044debd'
	#print(indicoio.sentiment_hq('indico is so easy to use!'))
	#filepath = "image0.jpg"
	#Image.LOAD_TRUNCATED_IMAGES = True
	#pixel_array = skimage.io.imread('filepath')
	image = Image.open(filepath)
	pixel_array = np.array(image)
	#print (indicoio.fer(pixel_array))
	return indicoio.fer(pixel_array)



if __name__ == '__main__':
    app.run(debug=True)
