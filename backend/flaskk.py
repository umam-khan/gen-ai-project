from flask import Flask, jsonify, request, session
from flask_cors import CORS
from translate import Translator
import speech_recognition as sr
import io
from ttsmms import TTS


app = Flask(__name__)
CORS(app)


def mp3_to_text_hindi(audio_content):
    recognizer = sr.Recognizer()
    audio_stream = io.BytesIO(audio_content)
    with sr.AudioFile(audio_stream) as source:
        print("Processing audio file...")
        audio = recognizer.record(source)
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio, language = 'hi-IN')
        return text
    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError as e:
        return f"Could not request results from Google Web Speech API; {e}"


@app.routes('/stt_hin', methods=['GET','POST'])
def stt_hin():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    audio_content = file.read()
    text = mp3_to_text_hindi(audio_content)
    session['prompthintext'] = text
    response = {'output':text}
    return jsonify(response)


def hin_to_eng(text):
    translator = Translator(to_lang="en", from_lang="hi")
    translated_text = translator.translate(text)
    return translated_text


@app.route("/tt_hin_eng",methods=["GET","POST"])
def tt_hin_eng():
    hin_text = session.get('propmthintext')
    if not hin_text:
        return jsonify({'error': 'Text not found in session'}), 400
    eng_text = hin_to_eng(hin_text)
    session['promptengtext'] = eng_text
    response = {'output':eng_text}
    return jsonify(response)


@app.route('/query_eng_pdf',methods=['POST','GET'])
def query_eng_pdf():
    query_prompt = session.get('promptengtext')
    query_result=""
    session['resultengtext'] = query_result
    response={'output':query_result}
    return jsonify(response)


def eng_to_hin(text):
    translator = Translator(to_lang="hi", from_lang="en")
    translated_text = translator.translate(text)
    return translated_text    


@app.route('/tt_eng_hin',methods=['POST','GET'])
def tt_eng_hin():
    query_result = session.get('resultengtext')
    if not query_result:
        return jsonify({'error': 'Text not found in session'}), 400
    hin_text = eng_to_hin(query_result)
    session['resulthintext'] = hin_text
    response = {'output':hin_text}
    return jsonify(response)

def hindi_text_to_mp3(text):
    dir_path = ("./models/hin")
    tts=TTS(dir_path)
    wav=tts.synthesis(text)
    return wav


#iske neeche kaam karna hai, calling of above function and defining of routes.


@app.route('/tts_hin',methods=['POST','GET'])
def tts_hin():

    response = {'output':'audiofile'}
    return jsonify(response)


@app.route('/stt_eng',methods=['GET','POST'])
def stt_eng():
    if request.method == 'POST':
        result=""
        response={'output':result}
        return jsonify(response)
    response={'output':'Server Error'}
    return jsonify(response)


@app.route('/tts_eng',methods=['GET','POST'])
def tts_eng():
    if request.method == 'POST':
        result=""
        response={'output':result}
        return jsonify(response)
    response={'output':'Server Error'}
    return jsonify(response)


if __name__== "__main__":
    app.run(debug=True)