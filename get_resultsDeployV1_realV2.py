"""
@author Liz
This is the helper class of version 2 of the app as deployed on streamlit cloud.
"""

import requests
from configure import *
# instruct user to send transcript file to chatGPT
import openai
import assemblyai as aai
import os
import sys
import time
from datetime import date
import streamlit as st
from dotenv import load_dotenv
sys.setrecursionlimit(2000)

openai.api_key = st.secrets["OPENAI_API_TOKEN"]


def auto_upload_to_AssemblyAI(filepath, sC): # key, 
    load_dotenv()
    aai.settings.api_key = st.secrets["ASSEMBLY_API_TOKEN"]  
    config = aai.TranscriptionConfig(speaker_labels=True, speakers_expected = sC)
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(filepath, config)  # , speakers_expected = speakerCount
    return transcript

def load_text(file):
    # Read the contents of the uploaded file
    if file is not None:
        return file.getvalue().decode("utf-8")
    return ""

MODEL = 'gpt-4-0613'
SEED = 75

def summarize_text(text, instructions):
    response = openai.ChatCompletion.create(
        model=MODEL,
        seed=SEED,
        messages = [
            {"role": "system", "content": instructions },
            {"role": "user", "content": text}
            ]
        # prompt=f"Transcript: {text}\n\nInstructions: {instructions}\n\nSummary:",
        # max_tokens=150
    )
    return response['choices'][0]['message']['content']

    
def checkForFile():
    if os.path.isfile(r'recording.mp3'):
        uploaded_file = r'recording.mp3'
        return uploaded_file
    else:
        return None

# TODO incorporate progress bars or something into these functions
def processTranscript(textString, nPart):
    if len(textString) > 0:
        text = textString
        instruction = "Use the provided transcript of a patient encounter delimited by triple quotes to create a clinical note, with the sections Subjective, Objective, Assessment, and Plan. Only use information that is contained within the transcript. If there are parts of the clinical note that are not contained within the transcript, do not include them in your input, and instead indicate that they are not included in the transcript."
        clinNote = summarize_text(text, instruction)
        ptpbText = "Creating encounter note..."
        ptpb = st.progress(0, text = ptpbText)
        for percent_complete2 in range(100):
            time.sleep(0.01)
            ptpb.progress(percent_complete2 + 1, text = ptpbText)
        st.write("Clinical Note from Transcript")
        # st.markdown(f'<p style="color:lightyellow;font-size:48px;">{clinNoteF}</p>', unsafe_allow_html=True)
        st.write(clinNote)
        # st.write(f'<style font-size:32px;>{clinNote}</style>')

        st.write("Procees complete")

def processAudioFile(aFile, speakerCount):
    textString = ""
    afpbText = "Creating encounter transcript..."
    if aFile is not None:
        afpb = st.progress(0, text = afpbText)
        print('in if clause...')
        nameString = 'recording.mp3' 
        # nPartsP = nameString.split('/')
        # nParts = nPartsP[len(nPartsP) - 1].split('.')
        # print('here is nParts name: ' + nParts[0])
        transcript = auto_upload_to_AssemblyAI(aFile, speakerCount) # aai.settings.api_key,
        print(transcript.text)
        for percent_complete in range(100):
            time.sleep(0.01)
            afpb.progress(percent_complete + 1, text = afpbText)
        for utterance in transcript.utterances:
            textString += f"Speaker {utterance.speaker}: {utterance.text}"
            textString += '\n'
        print('past file and textString creation')
        processTranscript(textString, nameString)
        
    else:
        print('in else clause...')
        time.sleep(5)
        processAudioFile(checkForFile(), speakerCount)

