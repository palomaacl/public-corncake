# web PythonAnywhere version

import sys
import os
sys.path.append('/home/palomaacl/corncake')
from flask import Flask, request, render_template, redirect
from thunderclass import ThunderBlade
from requests_oauthlib import OAuth2Session
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    global oauth, oauth_token
    client_id = os.environ["client_id"]
    client_secret = os.environ["client_secret"]
    redirect_url = "https://freesound.org/home/app_permissions/permission_granted/"

    #do the OAuth dance, required to download the sound samples directly
    #the rest of the authentication is performed on the backend, where Freesound is actually used
    oauth = OAuth2Session(client_id)
    code = request.values.get('auth_form')
    if code is not None:
        oauth_token = oauth.fetch_token("https://freesound.org/apiv2/oauth2/access_token/", code, client_secret=client_secret)
        ThunderBlade.get_auth(oauth_token)
    return render_template('authentication.html')

@app.route('/corncake', methods=['GET', 'POST'])
def corncake():
    #when the form is filled, sets the var and calls the function to set it on the backend
    if request.args.get("wordform") is not None:
        word_to_tr = request.values.get('wordform')
        ThunderBlade.set_word(word_to_tr)
    elif request.args.get("get_sound") is not None:
        return redirect('/sound')
    elif request.args.get("translate") is not None:
        return redirect('/translate')
    return render_template('index.html')

#both of these methods have sleep on them to make time for serverside operations to take place before redirect
@app.route('/translate', methods=['GET', 'POST'])
def translate():
    ThunderBlade.get_word()
    time.sleep(3)
    return redirect('/corncake')

@app.route('/sound', methods=['GET'])
def sound():
    ThunderBlade.get_sound()
    time.sleep(3)
    return redirect('/corncake')


if __name__ == '__main__':
    #app.run(debug=True)
    app.run()

