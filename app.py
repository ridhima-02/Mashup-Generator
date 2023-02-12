from flask import Flask, render_template, request
from prog import download_videos, convertToAudio, makeMashup, generateMashup
from email.message import EmailMessage
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import ssl
import smtplib
import os
import shutil
import io
import zipfile
import glob

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'static/files'


email_sender = 'ridhimagupta0212@gmail.com'
email_password = 'kjbcvowevbzfbdwc'


em = EmailMessage()
em['From'] = email_sender
em['Subject'] = 'Your Mashup output'
em.set_content(
    "This is the mashup audio. Thank you for using mashup generator.")

context = ssl.create_default_context()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def getData():
    singerName = request.form['singerName']
    vid = request.form['vid']
    duration = request.form['duration']
    email = request.form['email']

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as myzip:
        myzip.write("static/files/result.mp3", arcname="result.mp3")
    buffer.seek(0)

    with open("static/files/result.zip", "wb") as f:
        f.write(buffer.read())

    try:
        generateMashup(singerName, vid, duration)
    except:
        return "Error generated in function"

    try:
        with open("static/files/result.zip", 'rb') as fp:
            file_data = fp.read()
        em.add_attachment(file_data, maintype='application',
                          subtype='mp3', filename="result.zip")

        email_receiver = email
        em['To'] = email_receiver
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(em)

        # os.remove("static/files/result.mp3")
    except:
        return "Error occured!"

    return "Email sent"


if __name__ == '__main__':
    app.run(debug=True)
