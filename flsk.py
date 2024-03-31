from flask import Flask, render_template, request
import vertexai
from vertexai.generative_models import GenerativeModel, Part, Image

import os

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './')

app = Flask(__name__, template_folder=template_path, static_folder=project_root)
app.config['UPLOAD_FOLDER'] = './uploaded'

# app = Flask(__name__)

@app.route('/')
def home():
    return render_template('genai.html')

# handle get method
@app.route('/handle_post', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        imagefile = request.files.get('mediaFile', '')
        # file = request.files['file']
        file_type = str(type(imagefile))
        print(file_type)
        print(imagefile.filename)
        imagefile.save(os.path.join(app.config['UPLOAD_FOLDER'], imagefile.filename))
        image = Image.load_from_file(os.path.join(app.config['UPLOAD_FOLDER'], imagefile.filename))
        
        vertexai.init(project="testing-testing-393023", location="us-west4")

        # Load the model
        model = GenerativeModel(model_name="gemini-pro-vision")

        # Query the model
        response = model.generate_content([image, "Is this 'trash', 'recycling' or 'organic'? You must respond with one of the previous three options."])
        print(response.text)
        print(type(response.text))

        return render_template('genai_second.html', waste_type=response.text, img=os.path.join(app.config['UPLOAD_FOLDER'], imagefile.filename))

    else:
        return render_template('genai.html')


if __name__ == '__main__':
   app.run(port=5500)
