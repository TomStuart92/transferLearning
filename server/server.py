from flask import Flask, request, jsonify
from lib import classify_image

app = Flask(__name__, static_url_path='')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET'])
def get():
    return app.send_static_file('index.html'), 200


@app.route("/", methods=['POST'])
def post():
    if 'image' not in request.files:
      return jsonify({ 'error': 'No File Uploaded', 'resolution': 'Use Multipart form upload with data labelled image' }), 400

    file = request.files['image']

    if not allowed_file(file.filename):
      return jsonify({ 'error': 'Extension Not Allowed', 'resolution': 'Supported Uploads are .png, .jpg and .jpeg' }), 400

    output = classify_image.run(file)
    return jsonify(output), 200
