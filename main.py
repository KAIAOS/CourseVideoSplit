import os
import sys
import cv2
import json
import datetime
import difflib
from slicer import VideoSlicer
from searcher import get_details
from model import text_rec, text_detect
from ffmpy import FFmpeg
from scipy.io import wavfile
import speech_recognition as sr
from pydub import AudioSegment

def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


def dump(shot_details: list, dst: str):
    with open(dst, 'w') as fp:
        detail_list = [detail.__dict__ for detail in shot_details]
        for i in range(len(detail_list)):
            del detail_list[i]['frame']
            del detail_list[i]['texts']
            #detail_list[i]['texts'] = [text.__dict__ for text in detail_list[i]['texts']]
        json_str = json.dumps(detail_list)
        fp.write(json_str)


def process(video_path: str): #video_path单个视频路径

    video = cv2.VideoCapture(video_path)
    duration = video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS)

    # extract audio from video
    audio_path = video_path[: video_path.rfind('.')] + '.wav'
    if not os.path.exists(audio_path):
        ff = FFmpeg(
            inputs={video_path: None},
            outputs={audio_path: '-f wav -ar 16000'}
        )
        ff.run()

    # Split Video to frames by audio
    slicer = VideoSlicer()
    # samplerate, data = wavfile.read(audio_path)
    # audio = data[:, 0]
    frames = slicer.cut_video(video)
    """
    # Split Video to frames by 5s
    slicer = VideoSlicer()
    frames = slicer.cut_video(video)
    """
    # d&r text
    texts = []

    for pos, frame in frames:
        rects = text_detect(frame)
        text = text_rec(frame, rects)
        text_fliter = []
        for r in text:
            if r['cx'] > 565 and r['cy'] < 38:
                continue
            text_fliter.append(r)
        texts.append(text_fliter)

    # pick frames to fragment
    assert len(frames) == len(texts)
    flags = []
    for i in range(len(frames)-1):
        string1 = ''
        string2 = ''
        for item in texts[i]:
            string1 += item['text']
        for item in texts[i+1]:
            string2 += item['text']

        if string_similar(string1, string2) < 0.8:
            if len(string1) < len(string2):
                if string_similar(string1,string2[:len(string1)]) > 0.7:
                    continue
            flags.append(i+1)
        if i+1 == len(frames)-1 and flags[-1]!=len(frames)-1:
            flags.append(i+1)

    # format & classify text
    res = get_details(flags, duration, frames, texts)
    return res


def process_audio(video_path: str, res: list):
    r = sr.Recognizer()
    audio_path = video_path[: video_path.rfind('.')] + '.wav'
    if not os.path.exists(audio_path):
        ff = FFmpeg(
            inputs={video_path: None},
            outputs={audio_path: '-f wav -ar 16000'}
        )
        ff.run()
    file_path, file_name = os.path.split(audio_path)
    temp_path = os.path.join(file_path, 'temp')
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    sound = AudioSegment.from_wav(audio_path)

    #process each fragment
    for i, item in enumerate(res):
        if item.type != item.kShotTypeExample:
            continue
        start_time = item.start_time
        end_time = item.end_time
        start = int(start_time.split(':')[0])*60 + int(start_time.split(':')[1])
        end = int(end_time.split(':')[0])*60 + int(end_time.split(':')[1])
        fragment_name = file_name[: file_name.rfind('.')] + str(i) + '@' + str(start)+ '-' + str(end) + '.wav'
        fragment_path = os.path.join(temp_path, fragment_name)
        fragment = sound[start*1000: end*1000]
        fragment.export(fragment_path, format='wav')
        with sr.AudioFile(fragment_path) as source:
            fragment_audio = r.record(source)
        try:
            result = r.recognize_google(fragment_audio, language='zh-CN')
            item.audio_paragraph = str(result)
        except sr.UnknownValueError:
            print("Could not understand")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

    return res


def get_all_video(path: str) -> list:
    res = list()
    for root, _, files in os.walk(path):
        if root != path:
            continue
        for name in files:
            if name.endswith('.mp4'):
                res.append(os.path.join(root, name))
    return res


def main(argv):
    # path = '/home/henrylee/remote/cpu-node3/course_videos/WHU-1001539003/[第1周：绪论（时长：56分11秒）] 第1周第5讲-算法分析基础（11：19）.mp4'
    path = 'course_videos/test_video'
    video_files = get_all_video(path)

    t1 = datetime.datetime.now()
    print('-'*80)
    print('start at', t1.strftime('%H:%M'))
    i = 0
    for video_file in video_files:
        print("\t{}/{}: {}".format(i, len(video_files), video_file))
        t2 = datetime.datetime.now()
        res = process(video_file)
        res = process_audio(video_file, res)
        dump(res, video_file[: video_file.rfind('.')] + '.json')
        i += 1
        counter = 0
        for shot in res:
            if shot.type == shot.kShotTypeExample:
                print("\t\texamples found: {}@{}->{}".format(shot.abstract, shot.start_time, shot.end_time))
                counter += 1
        print("\t\ttime consume: ", datetime.datetime.now() - t2)
        print("\t\texamples count:", counter)
    print('end at', datetime.datetime.now().strftime('%H:%M'))
    print("total time: ", datetime.datetime.now() - t1)


if __name__ == '__main__':
    main(sys.argv)
