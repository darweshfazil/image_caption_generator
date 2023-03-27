from flask import Flask, request, render_template, session
from werkzeug.utils import secure_filename
import os
import predict as pred

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'Random12$@'

# route to landing page
@app.route('/')
def index():
    return render_template('image.html')
 
# route to upload file
@app.route('/',  methods=["POST", "GET"])
def uploadFile():
    if request.method == 'POST':
        uploaded_img = request.files['uploaded-file']
        session['uploaded_image_name'] = uploaded_img.filename
        img_filename = secure_filename(uploaded_img.filename)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
 
        return render_template('image2.html')
 
#route to generate caption with the uploaded file
@app.route('/getCaption')
def displayImage():
    img_file_path = session.get('uploaded_img_file_path', None)
    image_name = session.get('uploaded_image_name')
    generatedCaption = pred.generate_caption(image_name)
    return render_template('show.html', user_image = img_file_path, caption = generatedCaption)

# route to serve requests across platforms
@app.route('/generateCaption', methods=['POST'])
def getCaption():
    pred.initialize()
    uploaded_img = request.files['uploaded-file']
    img_filename = secure_filename(uploaded_img.filename)
    IMAGE_PATH = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
    uploaded_img.save(IMAGE_PATH)
    generatedCaption = pred.generate_caption(uploaded_img.filename)
    return generatedCaption

if __name__ == '__main__' :
    app.run(debug=False, host='0.0.0.0')