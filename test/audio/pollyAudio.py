import boto3
#from utteranceIO import *
import os
import glob
import random
import re

polly_client = boto3.Session(
                aws_access_key_id='YOUR KEY',                     
    aws_secret_access_key= 'YOUR KEY',
    region_name='us-east-1').client('polly')
filename = 'FILENAME'
filePath = str(filename)
s = open(filePath).read()
fullSetRead = eval(s)
newSet = {}
#phase 1
count1 = 0
au = ''
f= open("A BATCH FILE","w+")
f.write("echo off \r\n")
tempFileN = ""
command1 = "start "
for k1, k2 in fullSetRead.iteritems():
	if k1[4] == 0: #
		num = k1[3]
		print('number is ' + str(num))
		print k2
		temp = " Here is " + str(num) 
		temp1 = temp + ", application!!  "
		print temp1
		response = polly_client.synthesize_speech(VoiceId='Joanna', OutputFormat='mp3', Text = temp1)
		au = 'gaudioUsing1/seq' + str(num)
		audioFileName = au + '.mp3'
		file = open(audioFileName, 'w')
		file.write(response['AudioStream'].read())
		file.close()
		response = polly_client.synthesize_speech(VoiceId='Joanna',
		OutputFormat='mp3', 
		Text = ' ' + str(k2) )
		au = 'gaudioUsing1/au' + str(num)
		audioFileName = au + '.mp3'
		file = open(audioFileName, 'w')
		file.write(response['AudioStream'].read())
		file.close()
			# batch
		tempFileS = "seq" + str(num)
		tempFileS = tempFileS + ".mp3\r\n"
		temp = command1 + tempFileS 
		f.write(temp)
		f.write("timeout 3\r\n")
		tempFileN = "au" + str(num)
		tempFileN = tempFileN + ".mp3\r\n"
		temp = command1 + tempFileN 
		f.write(temp)
		f.write("timeout 12\r\n")
		f.write("start stopQ.mp3\r\n")
		f.write("timeout 5\r\n")
		f.write("start stop1.mp3\r\n")
		f.write("timeout 4\r\n")
		if num%5 == 0:
			f.write("start stop2.mp3\r\n")
			f.write("timeout 6\r\n")
f.write('pause\n')
f.close()
# ~ for vc in setRead:
	# ~ print setRead[vc]
	# ~ response = polly_client.synthesize_speech(VoiceId='Joanna',
        # ~ OutputFormat='mp3', 
        # ~ Text = str(setRead[vc]))
	# ~ au = 'audioUsing/au' + str(vc)
	# ~ audioFileName = au + '.mp3'
	# ~ file = open(audioFileName, 'w')
	# ~ file.write(response['AudioStream'].read())
	# ~ file.close()
# ~ #print newSet


译
