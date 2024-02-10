#main imports
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai

#custom function imports
from functions.text_to_speech import convert_text_to_speech
from functions.database import store_messages, reset_messages
from functions.openai_requests import convert_audio_to_text, get_chat_response


#initiate app
app = FastAPI()

#cors - origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:4174",
    "http://localhost:3000"
]

#cors - middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def check_health():
    return {"message": "Healthy"}

#reset the messages
@app.get("/reset")
async def reset_convo():
    reset_messages()
    return {"message": "convo reset"}

# #post bot response, not in browser
# @app.post("/post-audio")
# async def post_audio(file: UploadFile = File(...)):
#     print("hello")

#get route for now
@app.post("/post-audio")
async def post_audio(file: UploadFile = File(...)):

    #get saved audio
    # audio_input = open("voice.mp3","rb")

    #save file from frontend
    with open(file.filename,"wb") as buffer:
        buffer.write(file.file.read())
    audio_input= open(file.filename,"rb")


    #decode audio
    message_decoded=convert_audio_to_text(audio_input)

    print(message_decoded)

    #get chatgpt response 

    chat_response = get_chat_response(message_decoded)

    #store messages
    store_messages(message_decoded,chat_response)

    #convert chat response to audio
    print(chat_response)
    audio_output = convert_text_to_speech(chat_response)
    
    #create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    #return audio file
    return StreamingResponse(iterfile(),media_type="application/octet-stream")

