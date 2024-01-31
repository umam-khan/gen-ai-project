from flask import Flask, request
import os

from flask_cors import CORS
# routes
app= Flask(__name__)

CORS(app)

@app.route('/getaudio', methods=['POST'])
def receive_audio():
    try:
        audio_file = request.files['audio']
        # Save the audio file to the current folder
        audio_file.save(os.path.join(os.getcwd(), 'recordedAudio.weba'))
        return 'Audio received and saved successfully', 200
    except Exception as e:
        print(f'Error receiving audio: {e}')
        return 'Failed to receive audio', 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
