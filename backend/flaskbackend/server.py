from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
from translate import Translator
import os, io, base64
from pydub import AudioSegment
import speech_recognition as sr
import soundfile as sf
from rag import *
from viva import *
from summ import *
from gtts import gTTS
import uuid

app = Flask(__name__)
CORS(app)

HUGGINGFACE_API_KEY = os.getenv('HUGGING_FACE_KEY')

###GET PDF 
@app.route('/getpdf', methods=['POST'])
def get_pdf():
    try:
        pdf_file = request.files.get('pdf')
        print(pdf_file)
        if pdf_file:
            directory_path="C:\\Users\\Anand\\Desktop\\hack\\gen-ai-project\\backend\\flaskbackend\\data"
            pdf_file.save(os.path.join( directory_path, f'data{uuid.uuid4()}.pdf'))
            print('PDF file saved successfully')
            raw_text = read_pdfs_in_directory(directory_path)
            text_chunks = get_text_chunks(raw_text)
            get_vector_store(text_chunks)
            return jsonify({"success": True, "message": "PDF received and saved successfully"})

    except Exception as e:
        print(f"Error: {str(e)}")

    return jsonify({"success": False, "message": "Error processing PDF"})

##get AUDIO
@app.route('/audio2', methods=['GET'])
def serve_audio():
    file_path = "C:\\Users\\Anand\\Desktop\\hack\\gen-ai-project\\backend\\flaskbackend/final_output.wav"
    return send_file(file_path, mimetype='audio/wav')

#get getaudio
def mp3_to_text_hindi(data):
    print("Generating transcript")
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    headers = {"Authorization": HUGGINGFACE_API_KEY}
    response = requests.post(API_URL, headers=headers, data=data)
    result =  response.json()
    return result['text']


def english_to_hindi(english_text):
    print("translating")
    translator = Translator(to_lang="hi", from_lang='en')
    translated_text = translator.translate(english_text)
    return translated_text


def hindi_text_to_mp3(text):
    print("generating audio")
    language = 'hi'
    speed = False
    tts = gTTS(text=text, lang=language, slow=speed)
    tts.save("output.mp3")
    audio = AudioSegment.from_mp3("output.mp3")
    audio.export("final_output.wav", format="wav")
    import os
    os.remove("output.mp3")
    return "done"


def mp3_to_text_english(data):
    print("generating text")
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    headers = {"Authorization": HUGGINGFACE_API_KEY}
    response = requests.post(API_URL, headers=headers, data=data)
    result= response.json()
    return result['text']


def english_text_to_mp3(text):
    print("generating audio")
    language = 'en'
    speed = False
    tts = gTTS(text=text, lang=language, slow=speed)
    tts.save("output.mp3")
    audio = AudioSegment.from_mp3("output.mp3")
    audio.export("final_output.wav", format="wav")
    import os
    os.remove("output.mp3")
    return "done"


def mp3_to_text_marathi(data):
    print("generating text")
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    headers = {"Authorization": HUGGINGFACE_API_KEY}
    response = requests.post(API_URL, headers=headers, data=data)
    result =  response.json()
    return result['text']

def english_to_marathi(english_text):
    print("translating")
    translator = Translator(to_lang="mr", from_lang='en')
    translated_text = translator.translate(english_text)
    return translated_text


def marathi_text_to_mp3(text):
    print("generating audio")
    language = 'mr'
    speed = False
    tts = gTTS(text=text, lang=language, slow=speed)
    tts.save("output.mp3")
    audio = AudioSegment.from_mp3("output.mp3")
    audio.export("final_output.wav", format="wav")
    import os
    os.remove("output.mp3")
    return "done"


def mp3_to_text_tamil(data):
    print("generating text")
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    headers = {"Authorization": HUGGINGFACE_API_KEY}
    response = requests.post(API_URL, headers=headers, data=data)
    result =  response.json()
    return result['text']

def english_to_tamil(english_text):
    print("translating")
    translator = Translator(to_lang="ta", from_lang='en')
    translated_text = translator.translate(english_text)
    return translated_text


def tamil_text_to_mp3(text):
    print("generating audio")
    language = 'ta'
    speed = False
    tts = gTTS(text=text, lang=language, slow=speed)
    tts.save("output.mp3")
    audio = AudioSegment.from_mp3("output.mp3")
    audio.export("final_output.wav", format="wav")
    import os
    os.remove("output.mp3")
    return "done"

#getaudio
@app.route('/getaudio', methods=['POST','GET'])
def getaudio():
    try:
        input_lang = request.form.get('language')
        audio_file = request.files['audio']
        filename = f"recordedAudio_{uuid.uuid4()}.weba"
        audio_file.save(os.path.join(os.getcwd(), filename))
        audio = AudioSegment.from_file(filename, format="webm")
        sf.write("output.wav", audio.get_array_of_samples(), audio.frame_rate)
        file_path="output.wav"
        if input_lang=='hindi':
            with open(file_path, "rb") as f:
                data = f.read()
            stt_hindi=''
            stt_hindi = mp3_to_text_hindi(data)
            print(stt_hindi)
            print('\n\n')
            text_query_pdf = starting_point(stt_hindi)
            tt_eng_hin = english_to_hindi(text_query_pdf)#replace tt_hin_eng with text_query_pdf
            print(tt_eng_hin)
            print('\n\n')
            tts_hindi = hindi_text_to_mp3(tt_eng_hin)
            print(tts_hindi)
            print('\n\n')
            return jsonify({"text":tt_eng_hin, "success": True})
        elif input_lang == 'marathi':
            with open(file_path, "rb") as f:
                data = f.read()
            stt_marathi=''
            stt_marathi = mp3_to_text_marathi(data)
            print(stt_marathi)
            print('\n\n')
            text_query_pdf = starting_point(stt_marathi)
            tt_eng_mar = english_to_marathi(text_query_pdf)#replace tt_hin_eng with text_query_pdf
            print(tt_eng_mar)
            print('\n\n')
            tts_mar = marathi_text_to_mp3(tt_eng_mar)
            print(tts_mar)
            print('\n\n')
            return jsonify({"text":tt_eng_mar, "success": True})
        elif input_lang == 'tamil':
            with open(file_path, "rb") as f:
                data = f.read()
            stt_tamil=''
            stt_tamil = mp3_to_text_tamil(data)
            print(stt_tamil)
            print('\n\n')
            text_query_pdf = starting_point(stt_tamil)
            tt_eng_tam = english_to_tamil(text_query_pdf)#replace tt_hin_eng with text_query_pdf
            print(tt_eng_tam)
            print('\n\n')
            tts_tamil = tamil_text_to_mp3(tt_eng_tam)
            print(tts_tamil)
            print('\n\n')
            return jsonify({"text":tt_eng_tam, "success": True})
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

#getviva
@app.route('/getviva', methods=['POST','GET'])
def getviva():
    try:
        question="Generate Viva Questions"
        viva_result = main_viva(question)   
        return jsonify({"english":viva_result,"success":True})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"success": False, "message": "Error"})    

#getsummary
@app.route('/getsummary',methods=['POST','GET'])
def getsummmary():
    try:
        question="Generate Summary"
        summ_result = mainsumm(question)        
        return jsonify({"english":summ_result,"success":True})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"success": False, "message": "Error"}) 
    

def hindi_to_english(english_text):
    translator = Translator(to_lang="en", from_lang='hi')
    translated_text = translator.translate(english_text)
    return translated_text


def marathi_to_english(english_text):
    translator = Translator(to_lang="en", from_lang='mr')
    translated_text = translator.translate(english_text)
    return translated_text    


def tamil_to_english(english_text):
    translator = Translator(to_lang="en", from_lang='ta')
    translated_text = translator.translate(english_text)
    return translated_text    


#gettext
@app.route('/gettext', methods=['POST','GET'])
def gettext():
    try:
        input_text= request.form.get('text')
        input_lang = request.form.get('language')
        if input_lang=='hindi':
            tt_hin_eng = hindi_to_english(input_text)
            text_query_pdf = starting_point(tt_hin_eng)
            tt_eng_hin = english_to_hindi(text_query_pdf)
            return jsonify({"text":tt_eng_hin,"success":True})
        elif input_lang=='marathi':
            tt_mar_eng = marathi_to_english(input_text)
            print(tt_mar_eng)
            text_query_pdf = starting_point(tt_mar_eng)
            print(text_query_pdf)
            tt_eng_mar = english_to_marathi(text_query_pdf)
            return jsonify({"text":tt_eng_mar,"success":True})  
        elif input_lang=='tamil':
            tt_hin_eng = tamil_to_english(input_text)
            text_query_pdf = starting_point(tt_hin_eng)
            tt_eng_hin = english_to_tamil(text_query_pdf)
            return jsonify({"text":tt_eng_hin,"success":True})              
        else:
            text_query_pdf = starting_point(input_text)
            return jsonify({"text":text_query_pdf,"success":True})
    except Exception as e:
        print(f"Error: {str(e)}")

    return jsonify({"success": False, "message": "Error"}) 


if __name__ == '__main__':
    app.run(debug=True, port=5000)