# Imported Libraries
import speech_recognition as sr
from os import path, mkdir, listdir
from pydub import AudioSegment

# MacOS Path TO BE CONFIGURED BY USER!!!!
base_path = '/Users/nicolasromano/Documents/Documents - Nicolas’s MacBook Pro/code/AlgoRhythms/Digital_Audio/sound_files/car_thoughts/sept17/'
audio_title = 'electronic_music_as_a_model_for_visual_art.m4a'

# Path to Original audio file (recorded on Voice Memos as .m4a)
m4a_file = base_path + audio_title
# Location to google cloud JSON credentials
GOOGLE_CLOUD_SPEECH_CREDENTIALS = '/Users/nicolasromano/Documents/Documents - Nicolas’s MacBook Pro/code/AlgoRhythms/Digital_Audio/car_thoughts_transcriptions/serene-coyote-346200-4ce0fdf7b3b7.json'

# Convert .m4a to .wav and save to the same directory as original .m4a file
wav_file = AudioSegment.from_file(m4a_file, format='m4a')
wav_path = f'{m4a_file[0:-3]}wav'
file_handle = wav_file.export(wav_path, format='wav')

###########################################################################
# Break up audio file of variable length into N 1-min .wav segments  
# All 1-min clips get added to a sub-directory called 'minute clips       
###########################################################################
file_duration_secs = int(len(wav_file) / 1000)
file_duration_secs

try:
    mkdir(base_path + 'minute_clips') # folder to store 1 min MAX segmented clips
except FileExistsError:
    pass # path already made
start = 0
end = 60

while end <= file_duration_secs:
    t1 = start
    t2 = end # first 2 mins

    t1 = t1 * 1000 #Works in milliseconds
    t2 = t2 * 1000
    newAudio = AudioSegment.from_wav(wav_path)
    newAudio = newAudio[t1:t2]

    newAudio.export(f'{base_path}/minute_clips/{int(end / 60) - 1}.wav', format="wav") #Exports to a wav file in the current path.

    start += 60
    end += 60

#######################################################################################################
audio_files = []
for i in range(0, len(listdir(f'{base_path}/minute_clips'))):
    audio_files.append(f'{base_path}/minute_clips/{i}.wav')

# Read each of the 1 minute clips and pass through googles speech to text algorithm
# As it is being read, a transcription txt file is generated such that each
# 1 min transcription is added to a new line
# Google only allows for 1min chunks at a time!
# the transcription file is given the same name as the original audio file title but as .txt
s = 15 # to be used if there is a reading error and need to resume by skipping one of the n-minute clips
first_file = True
for path in audio_files[s:]:
    if first_file:
        transcription_filename = f"{audio_title[:-4]}.txt"
        transcription = open(transcription_filename, "w")
        r = sr.Recognizer()
        with sr.AudioFile(path) as source:
            audio = r.record(source)  # read the entire audio file

        txt_read = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)

        transcription.writelines(txt_read)
        transcription.close()
        first_file = False

    else:
        file1 = open(transcription_filename, "a")  # append mode
        r = sr.Recognizer()
        with sr.AudioFile(path) as source:
            audio = r.record(source)  # read the entire audio file

        txt_read = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)

        file1.write('\n' + txt_read)
        file1.close()
