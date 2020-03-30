import speech_recognition as sr
import datetime

def speech_to_text_cmu(audio_path: str):
    r = sr.Recognizer()
    language_type = "zh-CN"
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)
    try:
        return r.recognize_sphinx(audio, language=language_type)
    except sr.UnknownValueError:
        print("Could not understand")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))


if __name__ == '__main__':
    t1 = datetime.datetime.now()
    result = speech_to_text_cmu(audio_path="output1.wav")
    print(result)
    print(datetime.datetime.now()-t1)