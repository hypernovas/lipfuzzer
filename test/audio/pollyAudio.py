"""
Audio generation using Deepgram TTS.
Modernized replacement for AWS Polly.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tts.deepgram_tts import DeepgramTTS

# Initialize Deepgram TTS client
tts_client = DeepgramTTS()

# Configuration
filename = 'FILENAME'
filePath = str(filename)

# Read input data
s = open(filePath).read()
fullSetRead = eval(s)
newSet = {}

# Phase 1: Generate audio files
count1 = 0
au = ''

# Create batch file for automated playback
f = open("A_BATCH_FILE.bat", "w+")
f.write("echo off \r\n")
tempFileN = ""
command1 = "start "

for k1, k2 in fullSetRead.items():
    if k1[4] == 0:  # Filter condition
        num = k1[3]
        print(f'Processing number: {num}')
        print(k2)
        
        # Generate sequence announcement
        temp = f" Here is {num}"
        temp1 = temp + ", application!!  "
        print(temp1)
        
        # Synthesize sequence audio
        au = f'gaudioUsing1/seq{num}'
        audioFileName = au + '.mp3'
        
        # Ensure directory exists
        os.makedirs('gaudioUsing1', exist_ok=True)
        
        # Generate audio with Deepgram
        success = tts_client.synthesize(temp1, audioFileName)
        if success:
            print(f"Generated: {audioFileName}")
        else:
            print(f"Failed to generate: {audioFileName}")
        
        # Synthesize main utterance audio
        utterance_text = ' ' + str(k2)
        au = f'gaudioUsing1/au{num}'
        audioFileName = au + '.mp3'
        
        success = tts_client.synthesize(utterance_text, audioFileName)
        if success:
            print(f"Generated: {audioFileName}")
        else:
            print(f"Failed to generate: {audioFileName}")
        
        # Build batch file commands
        tempFileS = f"seq{num}.mp3\r\n"
        temp = command1 + tempFileS 
        f.write(temp)
        f.write("timeout 3\r\n")
        
        tempFileN = f"au{num}.mp3\r\n"
        temp = command1 + tempFileN 
        f.write(temp)
        f.write("timeout 12\r\n")
        
        f.write("start stopQ.mp3\r\n")
        f.write("timeout 5\r\n")
        
        f.write("start stop1.mp3\r\n")
        f.write("timeout 4\r\n")
        
        if num % 5 == 0:
            f.write("start stop2.mp3\r\n")
            f.write("timeout 6\r\n")

f.write('pause\n')
f.close()

print("\nAudio generation complete!")
print("Batch file created: A_BATCH_FILE.bat")
