import pandas as pd
import numpy as np
from flask import Flask, render_template, request, session, jsonify
import os
from werkzeug.utils import secure_filename
from mark_attendance import main_function
from json import JSONEncoder, dumps
from add_face import add_face


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyArrayEncoder, self).default(obj)


def flatten_list(lists):
    return [item for sublist in lists for item in sublist]


ENCODING_CSV = 'student_encodings.csv'
NAMES_CSV = 'student_names.csv'
UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
UPLOAD_FOLDER_FACES = os.path.join('staticFiles', 'registeredFaces')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_FACES'] = UPLOAD_FOLDER_FACES
app.secret_key = 'secret'


@app.route('/')
def index():
    return render_template('index_pg1.html')


@app.route('/register_face', methods=("POST", "GET"))
def register_face():
    if request.method == 'POST':
        uploaded_img = request.files['uploaded-file2']
        img_filename = secure_filename(uploaded_img.filename)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER_FACES'], img_filename))
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER_FACES'], img_filename)
        # name = add_face(session['uploaded_img_file_path'], NAMES_CSV, ENCODING_CSV)
        add_face(session['uploaded_img_file_path'], NAMES_CSV, ENCODING_CSV)
        os.remove(os.path.join(app.config['UPLOAD_FOLDER_FACES'], img_filename))
        # return jsonify({
        #     'registered to database': name
        # })
        return render_template('face_reg.html')



@app.route('/take_attendance', methods=("POST", "GET"))
def upload_file():
    if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['uploaded-file']
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        # Marking attendance of the uploaded image
        names, time, date = main_function(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        names = flatten_list(names)
        encoded_numpy_data = dumps(names, cls=NumpyArrayEncoder)

        # Removing image after marking attendance
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # return render_template('index_pg2.html')
        return jsonify({
            'attendance marked for': encoded_numpy_data,
            'at time': time,
            'at date': date
        })


@app.route('/show_list')
def display_attendance_list():
    attendance_file_path = 'staticFiles/Attendance.csv'
    df = pd.read_csv(attendance_file_path)
    df_html = df.to_html()
    return render_template('show_image.html', data_var=df_html)


if __name__ == '__main__':
    app.run(debug=True)
