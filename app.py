from flask import Flask, request, render_template, session
from werkzeug.utils import secure_filename
import os
import predict as p

app = Flask(__name__)

# Defining upload folder path
UPLOAD_FOLDER = os.path.join('static', 'uploads')

# Configure upload folder for Flask application
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define secret key to enable session
app.secret_key = 'Random12$@'

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/home')
def index():
    return render_template('image.html')
 
@app.route('/home',  methods=["POST", "GET"])
def uploadFile():
    if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['uploaded-file']
        session['uploaded_image_name'] = uploaded_img.filename
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
 
        return render_template('image2.html')
 
@app.route('/getCaption')
def displayImage():
    # Retrieving uploaded file path from session
    img_file_path = session.get('uploaded_img_file_path', None)
    image_name = session.get('uploaded_image_name')
    generatedCaption = p.generate_caption(image_name)
    # Display image in Flask application web page
    return render_template('show.html', user_image = img_file_path, caption = generatedCaption)

@app.route('/getCaption', methods=['POST'])
def getCaption():
    uploaded_img = request.files['uploaded-file']
    # Extracting uploaded data file name
    img_filename = secure_filename(uploaded_img.filename)
    IMAGE_PATH = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
    # Upload file to database (defined uploaded folder in static path)
    uploaded_img.save(IMAGE_PATH)
    generatedCaption = p.generate_caption(uploaded_img.filename)
    # Display image in Flask application web page
    return generatedCaption


def initialize():
    print("<-----This function will run once----->")

if __name__ == '__main__' :
    initialize()
    app.run(debug=False, host='0.0.0.0')