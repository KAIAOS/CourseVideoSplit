from scipy.io import wavfile
from pydub import AudioSegment
from pydub.silence import split_on_silence
from aip import AipSpeech
import speech_recognition as sr
import os

audio_path='course_videos/CUC-1206073804/[第一章 绪论] 第1讲 基本概念.wav'
file_path, file_name = os.path.split(audio_path)
temp_path = os.path.join(file_path,'temp')
client = AipSpeech('18916980', 'LDonbbm6l4VCnwRAdeKPhAUM', 'eVkEfdKyIp2BFyZL9aWvZmVxPav6qGF0')
sound = AudioSegment.from_wav('course_videos/CUC-1206073804/[第一章 绪论] 第1讲 基本概念.wav')
sound = sound[:0.5*60*1000]
# os.makedirs('course_videos/CUC-1206073804/temp')
# course_videos/CUC-1206073804/temp/[第一章 绪论] 第1讲 基本概念0@0:0-5:26.wav
sound.export('course_videos/CUC-1206073804/temp/[第一章 绪论] 第1讲 基本概念0@00-526.wav', format='wav')
# # chunks = split_on_silence(sound,min_silence_len=300,silence_thresh=-70)
# # d = client.asr(sound.raw_data, 'wav', 16000)
# # # result = d['result'][0]
# # print(d)
# r = sr.Recognizer()
# language_type = "zh-CN"
# source= sr.AudioFile(sound.raw_data)
# audio = r.record(source)
# print(r.recognize_sphinx(audio, language=language_type))
