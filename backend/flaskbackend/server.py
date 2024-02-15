from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
from deep_translator import GoogleTranslator
import os, io, base64
from pydub import AudioSegment
import speech_recognition as sr
import soundfile as sf
from rag import *
from viva import *
from summ import *
from gtts import gTTS
import uuid
from openai import OpenAI

app = Flask(__name__)
CORS(app)

HUGGINGFACE_API_KEY = os.getenv('HUGGING_FACE_KEY')
data_dir = os.getenv( 'DATA_DIR', './data/' )
fin_out = os.getenv('OUTPUT_DIR', './final_output.wav')
###GET PDF 
@app.route('/getpdf', methods=['POST'])
def get_pdf():
    try:
        pdf_file = request.files.get('pdf')
        print(pdf_file)
        if pdf_file:
            directory_path=data_dir
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
    file_path = fin_out
    return send_file(file_path, mimetype='audio/wav')

#get getaudio
def mp3_to_text_hindi(data):
    client = OpenAI(api_key="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")
    audio_file= open(data, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        language="hi",
        response_format="text"
    )
    return transcript


def english_to_hindi(english_text):
    print("translating")
    translated = GoogleTranslator(source='en',target='hi').translate(english_text)
    return translated


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
    client = OpenAI(api_key="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")
    audio_file= open(data, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        language="en",
        response_format="text"
    )
    return transcript


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
    client = OpenAI(api_key="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")
    audio_file= open(data, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        language="mr",
        response_format="text"
    )
    return transcript


def english_to_marathi(english_text):
    print("translating")
    translated = GoogleTranslator(source='en',target='mr').translate(english_text)
    return translated


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
    client = OpenAI(api_key="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")
    audio_file= open(data, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        language="ta",
        response_format="text"
    )
    return transcript

def english_to_tamil(english_text):
    print("translating")
    translated = GoogleTranslator(source='en',target='ta').translate(english_text)
    return translated


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


def hindi_to_english(english_text):
    translated = GoogleTranslator(source='hi',target='en').translate(english_text)
    return translated


def marathi_to_english(english_text):
    translated = GoogleTranslator(source='mr',target='en').translate(english_text)
    return translated  


def tamil_to_english(english_text):
    translated = GoogleTranslator(source='ta',target='en').translate(english_text)
    return translated  



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
            stt_hindi=''
            stt_hindi = mp3_to_text_hindi(file_path)
            print(stt_hindi)
            print('\n\n')
            tt_hin_eng = hindi_to_english(stt_hindi)
            print(tt_hin_eng)
            print('\n\n')
            text_query_pdf = starting_point(tt_hin_eng)
            print(text_query_pdf)
            print('\n\n')
            tt_eng_hin = english_to_hindi(text_query_pdf)#replace tt_hin_eng with text_query_pdf
            print(tt_eng_hin)
            print('\n\n')
            tts_hindi = hindi_text_to_mp3(tt_eng_hin)
            return jsonify({"text":tt_eng_hin, "success": True})
        elif input_lang == 'marathi':
            stt_marathi=''
            stt_marathi = mp3_to_text_marathi(file_path)
            print(stt_marathi)
            print('\n\n')
            tt_mar_eng = marathi_to_english(stt_marathi)
            print(tt_mar_eng)
            print('\n\n')
            text_query_pdf = starting_point(tt_mar_eng)
            print(text_query_pdf)
            print('\n\n')
            tt_eng_mar = english_to_marathi(text_query_pdf)#replace tt_hin_eng with text_query_pdf
            print(tt_eng_mar)
            print('\n\n')
            tts_mar = marathi_text_to_mp3(tt_eng_mar)
            print(tts_mar)
            print('\n\n')
            return jsonify({"text":tt_eng_mar, "success": True})
        elif input_lang == 'tamil':
            stt_tamil=''
            stt_tamil = mp3_to_text_tamil(file_path)
            print(stt_tamil)
            print('\n\n')
            tt_tam_eng = tamil_to_english(stt_tamil)
            print(tt_tam_eng)
            print('\n\n')
            text_query_pdf = starting_point(tt_tam_eng)
            print(text_query_pdf)
            print('\n\n')
            tt_eng_tam = english_to_tamil(text_query_pdf)#replace tt_hin_eng with text_query_pdf
            print(tt_eng_tam)
            print('\n\n')
            tts_tamil = tamil_text_to_mp3(tt_eng_tam)
            print(tts_tamil)
            print('\n\n')
            return jsonify({"text":tt_eng_tam, "success": True})
        else:
            stt_english = mp3_to_text_english(file_path)
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