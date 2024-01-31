from flask import Flask, jsonify, redirect, url_for, request
import requests
from flask_cors import CORS
import speech_recognition as sr
from translate import Translator
import io, base64
from pydub import AudioSegment
from ttsmms import TTS

app = Flask(__name__)
CORS(app)

audio_file = ".\Rev.mp3"

'''
def encode_mp3_to_base64(file_path):
    with open(file_path, 'rb') as mp3_file:
        mp3_binary_data = mp3_file.read()
        base64_encoded = base64.b64encode(mp3_binary_data)
        return base64_encoded.decode('utf-8')
'''    

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

def mp3_to_text_english(audio_content):
    recognizer = sr.Recognizer()
    audio_stream = io.BytesIO(audio_content)
    with sr.AudioFile(audio_stream) as source:
        print("Processing audio file...")
        audio = recognizer.record(source)
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio, language = 'en-US')
        return text
    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError as e:
        return f"Could not request results from Google Web Speech API; {e}"

def hindi_to_english(hindi_text):
    translator = Translator(to_lang="en", from_lang="hi")
    translated_text = translator.translate(hindi_text)
    return translated_text


def english_to_hindi(english_text):
    translator = Translator(to_lang="hi", from_lang='en')
    translated_text = translator.translate(english_text)
    return translated_text

def hindi_text_to_mp3(text):
    dir_path = ("./backend/models/hin")
    tts=TTS(dir_path)
    synthesized_wav=tts.synthesis(text)
    wav=synthesized_wav["x"]
    wav_binary = wav.tobytes()
    base64_encoded = base64.b64encode(wav_binary).decode('utf-8')
    return base64_encoded

def english_text_to_mp3(text):
    dir_path = ("./backend/models/eng")
    tts=TTS(dir_path)
    synthesized_wav=tts.synthesis(text)
    wav=synthesized_wav["x"]
    wav_binary = wav.tobytes()
    base64_encoded = base64.b64encode(wav_binary).decode('utf-8')
    return base64_encoded


@app.route('/get_result', methods=['GET','POST'])
def get_result():
    data = request.get_json()
    lang = data.get('lang')
    input_type = data.get('input_type')
    text = data.get('text')
    voice= data.get('audio')
    if lang=='hindi':
        if input_type=='speech':
            #base64encoded = encode_mp3_to_base64(audio_file)
            decoded = base64.b64decode(voice)
            audio = AudioSegment.from_mp3(io.BytesIO(decoded))
            wav_data = io.BytesIO()
            audio.export(wav_data, format="wav")
            wav_data.seek(0)
            stt_hindi = mp3_to_text_hindi(wav_data.read())
            print(stt_hindi)
            print('\n\n')
            tt_hin_eng = hindi_to_english(stt_hindi)
            print(tt_hin_eng)
            print('\n\n')
            #text_query_pdf = query_pdf(tt_hin_eng)
            tt_eng_hin = english_to_hindi(tt_hin_eng)#replace tt_hin_eng with text_query_pdf
            print(tt_eng_hin)
            print('\n\n')
            tts_hindi = hindi_text_to_mp3(tt_eng_hin)
            print('\n\n\n')
            return {'hindi_text':tt_eng_hin,'hindi_audio':tts_hindi}
        else:
            tt_hin_eng = hindi_to_english(text)
            #text_query_pdf = query_pdf(tt_hin_eng)
            tt_eng_hin = english_to_hindi(tt_hin_eng)#replace tt_hin_eng with text_query_pdf
            return {'hindi_text':tt_eng_hin}
    elif lang=='english':
        if input_type=='speech':
            #base64encoded = encode_mp3_to_base64(audio_file)
            decoded = base64.b64decode(voice)
            audio = AudioSegment.from_mp3(io.BytesIO(decoded))
            wav_data = io.BytesIO()
            audio.export(wav_data, format="wav")
            wav_data.seek(0)
            stt_english = mp3_to_text_english(wav_data.read())
            print(stt_english)
            print('\n\n')
            #text_query_pdf = query_pdf(stt_english)
            tts_english = english_text_to_mp3(stt_english)#replace stt_english with text_query_pdf
            return {'english_text':tt_eng_hin,'english_audio':tts_english}
        else:
            #text_query_pdf = query_pdf(text)
            return {'english_text':''}
                        


    
if __name__ == '__main__':
    app.run(debug=True)