"""
@author Liz
This is version 2 of the app as deployed on streamlit cloud.
"""


import streamlit as st
import requests
from get_resultsDeployV1_realV2 import *
from streamlit.components.v1 import html
import assemblyai as aai
import sys
import os
  
# TODO Make the app reload after recursion limit is reached


# javascript
my_js = """
let mediaRecorder;
let recordedChunks = [];

document.getElementById('startBtn').addEventListener('click', () => {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = event => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };
            mediaRecorder.start();
            document.getElementById('startBtn').disabled = true;
            document.getElementById('stopBtn').disabled = false;
            document.getElementById('downloadBtn').disabled = true;
        });
});

document.getElementById('stopBtn').addEventListener('click', () => {
    mediaRecorder.stop();
    mediaRecorder.onstop = () => {
        const audioBlob = new Blob(recordedChunks, { type: 'audio/mp3' });
        const audioUrl = URL.createObjectURL(audioBlob);
        const audioElement = document.getElementById('audioPlayback');
        audioElement.src = audioUrl;
        //const downloadLink = document.getElementById('downloadBtn');
        //downloadLink.href = audioUrl;
        //downloadLink.download = 'recording.mp3';
        document.getElementById('startBtn').disabled = false;
        document.getElementById('stopBtn').disabled = true;
        document.getElementById('downloadBtn').disabled = false;
    };
});

document.getElementById('downloadBtn').addEventListener('click', () => {
    const audioBlob = new Blob(recordedChunks, { type: 'audio/mp3' });
    const audioUrl = URL.createObjectURL(audioBlob);
    if (audioBlob && audioUrl) {
            const a = document.createElement('a');
            a.href = audioUrl;
            a.download = 'recording.mp3'
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            document.getElementById('startBtn').disabled = false;
            document.getElementById('stopBtn').disabled = true;
            document.getElementById('downloadBtn').disabled = true;
    }
    
    
});

"""

# Wrap the javascript as html code
my_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Voice Recorder</title>
</head>
<body style="font-family: Arial, sans-serif;
            text-align: center;
            margin: 50px;
            background-color: lightyellow;">
   <!-- <h1>Voice Recorder</h1> -->
    <button id="startBtn" style="margin: 10px;
                                background-color: lightblue;
                                font-size: 22px;">
                                Start Recording</button>
    <button id="stopBtn" disabled style="margin: 10px;
                                background-color: lightblue;
                                font-size: 22px;">Stop Recording</button>
    <button id="downloadBtn" disabled style="margin: 10px;
                                background-color: lightblue;
                                font-size: 22px;">Download Recording</button>
    <br>
    <audio id="audioPlayback" controls style=margin-top: 20px;></audio>

    <script>{my_js}</script>
</body>
</html>

"""
 #     


st.markdown(f'<h1 style="color:lightyellow;font-size:48px;">Ambient Note Maker</h1>', unsafe_allow_html=True)
# st.title('Ambient Note Maker')
st.markdown(f'<h2 style="color:lightyellow;font-size:24px;">To begin, record a visit using the Start Recording and Stop Recording buttons.</h2>', unsafe_allow_html=True)
st.markdown(f'<h2 style="color:lightyellow;font-size:24px;">Click the Download Recording button to begin the note creation process.</h2>', unsafe_allow_html=True)

# remove old file
if os.path.isfile(r'C:/Users/email/Downloads/recording.mp3'):
    os.remove(r'C:/Users/email/Downloads/recording.mp3')
    # os.rename(r'C:/Users/email/Downloads/recording.mp3', r'C:/Users/email/Downloads/recording_prev.mp3')

html(my_html)

genStyle = '''
<style>
    .stApp {
    background-color: #000066;
    color: lightyellow;
    font-size:32px;
    }
</style>
'''

st.markdown(genStyle, unsafe_allow_html=True)

pbStyle = '''
<style>
    .stProgress {
    background-color: lightyellow;
    color: darkblue;
    }
</style>
'''
st.markdown(pbStyle, unsafe_allow_html=True)

speakerCount = 1

# if speakerCount == 0:
#     speakerCount = 2

    
uploaded_file = None

if uploaded_file == None:
    processAudioFile(checkForFile(), speakerCount)




        



