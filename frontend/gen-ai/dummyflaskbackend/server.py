from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os

app = Flask(__name__)
CORS(app)

@app.route('/getinput', methods=['POST'])
def get_input():
    try:
        input_type = request.form.get('inputType')
        language = request.form.get('language')
        text = request.form.get('text')
        audio_base64 = request.form.get('audio')

        # Handle the data as needed
        print(f'Input Type: {input_type}')
        print(f'Language: {language}')
        print(f'Text: {text}')
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

@app.route('/getpdf', methods=['POST'])
def get_pdf():
    try:
        pdf_file = request.files.get('pdf')

        if pdf_file:
            pdf_file.save(os.path.join(os.getcwd(), 'uploaded_pdf.pdf'))
            print('PDF file saved successfully')

            return jsonify({"success": True, "message": "PDF received and saved successfully"})

    except Exception as e:
        print(f"Error: {str(e)}")

    return jsonify({"success": False, "message": "Error processing PDF"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
