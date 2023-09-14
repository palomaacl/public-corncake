import freesound
import os
from googletrans import Translator
from gtts import gTTS
from requests_oauthlib import OAuth2Session

class ThunderBlade:
    def set_word(word_to_tr):
        #gets the variable from the HTML form, uses it throughout the script
        global word
        word = word_to_tr

    def get_word():
        global word
        #translates the given parameter to the target language with the API
        translator = Translator()
        target = translator.translate(word, dest='it')
        #converts the text of the translation to speech, saves the audio file to a destination displayable by Flask
        target_trans = gTTS(text=target.text, lang='it', slow=False)
        target_trans.save("/home/palomaacl/mysite/static/translation.mp3")

    def get_auth(auth_code):
        #gets the Oauth token from the authentication HTML form, stores it for later use
        global oauth_token
        oauth_token = auth_code

    def get_sound():
        global word, oauth_token
        client_id = os.environ["client_id"]

        #complete the OAuth dance
        client = freesound.FreesoundClient()
        client.set_token(oauth_token["access_token"], "oauth")
        query = client.text_search(query="{%s}" % word,fields="id,name,previews,type",filter="duration:[0.0 TO 10.0]",page_size=1)
        for sound in query:
            # directly downloads the file. as the client is already authenticated before the query, requires nothing else
            sound.retrieve("/home/palomaacl/mysite/static/", name="sound.mp3")

# all paths used here relate to the locations of the server this application was originally configured in
# remember to adjust yours accordingly, especially saving the files to /static/, otherwise Flask doesn't recognize them

