from flask import Flask, request, jsonify
from flask_cors import CORS
from translate import Translator
import os, io, base64
from pydub import AudioSegment
import speech_recognition as sr
import ttsmms as TTS

app = Flask(__name__)
CORS(app)

@app.route('/getpdf', methods=['POST'])
def get_pdf():
    try:
        pdf_file = request.files.get('pdf')
        print(pdf_file)
        if pdf_file:
            pdf_file.save(os.path.join(os.getcwd(), 'uploaded_pdf.pdf'))
            print('PDF file saved successfully')

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


def mp3_to_text_hindi(audio_content):
    recognizer = sr.Recognizer()
    audio_stream = io.BytesIO(audio_content)
    text=''
    with sr.AudioFile(audio_stream) as source:
        print("Processing audio file...")
        audio = recognizer.record(source)
        print("Recognizing...")
        text = recognizer.recognize_google(audio, language = 'hi-IN')
    return text
    
    

def hindi_text_to_mp3(text):
    dir_path = ("./models/hin")
    tts=TTS(dir_path)
    synthesized_wav=tts.synthesis(text)
    wav=synthesized_wav["x"]
    wav_binary = wav.tobytes()
    base64_encoded = base64.b64encode(wav_binary).decode('utf-8')
    return base64_encoded


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
    dir_path = ("./models/eng")
    tts=TTS(dir_path)
    synthesized_wav=tts.synthesis(text)
    wav=synthesized_wav["x"]
    wav_binary = wav.tobytes()
    base64_encoded = base64.b64encode(wav_binary).decode('utf-8')
    return base64_encoded


def decode_audio(audio):
    decoded_audio = base64.b64decode(audio)
    return decoded_audio



@app.route('/getaudio', methods=['POST'])
def getaudio():
    try:
        input_type = request.form.get('inputType')
        language = request.form.get('language')
        text = request.form.get('text')
        audio_base64 = request.form.get('audio')

        # Handle the data as needed
        print(f'Language: {language}')
        print(f'Audio:{audio_base64}')
        # Save the audio to a file in the current folder
        if input_type == 'audio' and audio_base64:
            audio_binary = base64.b64decode(audio_base64.split(',')[1])
            with open('recordedAudio.weba', 'wb') as audio_file:
                audio_file.write(audio_binary)
            print('Audio saved successfully')

        return jsonify({"success": True, "message": "Data received successfully"})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"success": False, "message": "Error processing data"})

    '''
    try:
        input_audio= request.form.get('audio')
        input_lang = request.form.get('language')
        print(input_audio)
        if input_lang=='hindi':
            #base64encoded = encode_mp3_to_base64(audio_file)
            decoded = base64.b64decode(input_audio)
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
            decoded_answer_audio = decode_audio(tts_hindi)
            print('\n\n')
            return jsonify({'text':tt_eng_hin,'audio':decoded_answer_audio, "success": True})
        else:
            decoded = base64.b64decode(input_audio)
            audio = AudioSegment.from_mp3(io.BytesIO(decoded))
            wav_data = io.BytesIO()
            audio.export(wav_data, format="wav")
            wav_data.seek(0)
            stt_english = mp3_to_text_english(wav_data.read())
            print(stt_english)
            print('\n\n')
            #text_query_pdf = query_pdf(stt_english)
            tts_english = english_text_to_mp3(stt_english)#replace stt_english with text_query_pdf
            decoded_answer_audio = decode_audio(tts_english)
            return jsonify({"text":tt_eng_hin,"audio":decoded_answer_audio,"success": True})
    except Exception as e:
        print(f"Error: {str(e)}")

    return jsonify({"success": False, "message": "Error"})
'''


@app.route('/gettext', methods=['POST'])
def gettext():
    try:
        input_text= request.form.get('text')
        input_lang = request.form.get('language')
        print(input_text)
        print(input_lang)
        if input_lang=='hindi':
            tt_hin_eng = hindi_to_english(input_text)
            tt_eng_hin = english_to_hindi(tt_hin_eng)
            return jsonify({"text":tt_eng_hin,"success":True})
        else:
            return jsonify({"text":input_text,"success":True})
    except Exception as e:
        print(f"Error: {str(e)}")

    return jsonify({"success": False, "message": "Error"})    


if __name__ == '__main__':
    app.run(debug=True, port=5000)
