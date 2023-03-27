from flask import Flask, request, render_template, session
from werkzeug.utils import secure_filename
import os
import predict as p

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/home')
def index():
    return render_template('image.html')
 
@app.route('/home',  methods=["POST", "GET"])
def uploadFile():
    if request.method == 'POST':
        uploaded_img = request.files['uploaded-file']
        session['uploaded_image_name'] = uploaded_img.filename
        img_filename = secure_filename(uploaded_img.filename)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
 
        return render_template('image2.html')
 
@app.route('/getCaption')
def displayImage():
    img_file_path = session.get('uploaded_img_file_path', None)
    image_name = session.get('uploaded_image_name')
    generatedCaption = p.generate_caption(image_name)
    return render_template('show.html', user_image = img_file_path, caption = generatedCaption)

@app.route('/generateCaption', methods=['POST'])
def getCaption():
    uploaded_img = request.files['uploaded-file']
    img_filename = secure_filename(uploaded_img.filename)
    IMAGE_PATH = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
    uploaded_img.save(IMAGE_PATH)
    generatedCaption = p.generate_caption(uploaded_img.filename)
    return generatedCaption

def initialize():
    print("<-----This function will run once----->")

if __name__ == '__main__' :
    initialize()
    app.run(debug=False, host='0.0.0.0')