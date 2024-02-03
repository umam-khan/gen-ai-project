from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
from translate import Translator
import os, io, base64
from pydub import AudioSegment
import speech_recognition as sr
import soundfile as sf
from rag import *
from gtts import gTTS


app = Flask(__name__)
CORS(app)

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
headers = {"Authorization": "Bearer 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"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()
output = query("output.wav")

@app.route('/getpdf', methods=['POST'])
def get_pdf():
    try:
        pdf_file = request.files.get('pdf')
        print(pdf_file)
        if pdf_file:
            pdf_file.save(os.path.join(os.getcwd(), 'uploaded_pdf.pdf'))
            pdf_path = "C:\\Users\\Anand\\Desktop\\hack\\gen-ai-project\\frontend\\gen-ai\\dummyflaskbackend\\uploaded_pdf.pdf"
            print('PDF file saved successfully')
            raw_text = get_pdf_text(pdf_path)
            text_chunks = get_text_chunks(raw_text)
            get_vector_store(text_chunks)
            return jsonify({"success": True, "message": "PDF received and saved successfully"})

    except Exception as e:
        print(f"Error: {str(e)}")

    return jsonify({"success": False, "message": "Error processing PDF"})

def hindi_to_english(hindi_text):
    translator = Translator(to_lang="en", from_lang="hi")
    translated_text = translator.translate(hindi_text)
    return translated_text


def english_to_hindi(english_text):
    translator = Translator(to_lang="hi", from_lang='en')
    translated_text = translator.translate(english_text)
    return translated_text


def mp3_to_text_hindi(filename):
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    headers = {"Authorization": "Bearer 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"}
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    result = response.json()
    return result['text']

    

def hindi_text_to_mp3(text):
    language = 'hi'
    speed = False
    tts = gTTS(text=text, lang=language, slow=speed)
    tts.save("output.mp3")
    audio = AudioSegment.from_mp3("output.mp3")
    audio.export("final_output.wav", format="wav")
    import os
    os.remove("output.mp3")
    return "done"


def mp3_to_text_english(audio_content):
    recognizer = sr.Recognizer()
    audio_stream = io.BytesIO(audio_content)
    text=''
    with sr.AudioFile(audio_stream) as source:
        print("Processing audio file...")
        audio = recognizer.record(source)
        print("Recognizing...")
        text = recognizer.recognize_google(audio, language = 'en-US')
    return text


def english_text_to_mp3(text):
    language = 'en'
    speed = False
    tts = gTTS(text=text, lang=language, slow=speed)
    tts.save("output.mp3")
    audio = AudioSegment.from_mp3("output.mp3")
    audio.export("final_output.wav", format="wav")
    import os
    os.remove("output.mp3")
    return "done"



@app.route('/getaudio', methods=['POST'])
def getaudio():
    try:
        input_type = request.form.get('inputType')
        input_lang = request.form.get('language')
        text = request.form.get('text')
        audio_file = request.files['audio']
        audio_file.save(os.path.join(os.getcwd(), 'recordedAudio.weba'))
        audio = AudioSegment.from_file("recordedAudio.weba", format="webm")
        sf.write("output.wav", audio.get_array_of_samples(), audio.frame_rate)
        file_path="output.wav"
        if input_lang=='hindi':
            stt_hindi=''
            stt_hindi = mp3_to_text_hindi(file_path)
            print(stt_hindi)
            print('\n\n')
            tt_hin_eng = hindi_to_english(stt_hindi)
            print(tt_hin_eng)
            print('\n\n')
            text_query_pdf = starting_point(tt_hin_eng)
            tt_eng_hin = english_to_hindi(text_query_pdf)
            print(tt_eng_hin)
            print('\n\n')
            tts_hindi = hindi_text_to_mp3(tt_eng_hin)
            print(tts_hindi)
            print('\n\n')
            return jsonify({"text":tt_eng_hin, "success": True})
        else:
            with open(file_path, 'rb') as audio_file:
                audio_content = audio_file.read()
            stt_english = mp3_to_text_english(audio_content)
            print(stt_english)
            print('\n\n')
            text_query_pdf = starting_point(stt_english)
            print(text_query_pdf)
            tts_english = english_text_to_mp3(text_query_pdf)#replace stt_english with text_query_pdf
            print(tts_english)
            return jsonify({"text":text_query_pdf,"success": True})
    except Exception as e:
        print(f"Error: {str(e)}")

    return jsonify({"success": False, "message": "Error"})


@app.route('/audio')
def serve_audio():
    file_path = "C:/Users/Anand/Desktop/hack/gen-ai-project/frontend/gen-ai/dummyflaskbackend/final_output.wav"
    return send_file(file_path, mimetype='audio/wav')

@app.route('/gettext', methods=['POST'])
def gettext():
    try:
        input_text= request.form.get('text')
        input_lang = request.form.get('language')
        print(input_text)
        print(input_lang)
        if input_lang=='hindi':
            tt_hin_eng = hindi_to_english(input_text)
            text_query_pdf = starting_point(tt_hin_eng)
            tt_eng_hin = english_to_hindi(text_query_pdf)
            return jsonify({"text":text_query_pdf,"success":True})
        else:
            text_query_pdf = starting_point(input_text)
            return jsonify({"text":text_query_pdf,"success":True})
    except Exception as e:
        print(f"Error: {str(e)}")

    return jsonify({"success": False, "message": "Error"})    


if __name__ == '__main__':
    app.run(debug=True, port=5000)
