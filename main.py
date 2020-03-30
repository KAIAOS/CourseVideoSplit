import os
import sys
import cv2
import json
import datetime
import difflib
from slicer import VideoSlicer
from searcher import get_details
from model import text_rec, text_detect


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

def dump(shot_details: list, dst: str):
    with open(dst, 'w') as fp:
        detail_list = [detail.__dict__ for detail in shot_details]
        for i in range(len(detail_list)):
            del detail_list[i]['frame']
            detail_list[i]['texts'] = [text.__dict__ for text in detail_list[i]['texts']]
        json_str = json.dumps(detail_list)
        fp.write(json_str)


def process(video_path: str): #video_path单个视频路径

    video = cv2.VideoCapture(video_path)
    duration = video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS)

    # Split Video to frames
    slicer = VideoSlicer()
    frames = slicer.cut_video(video)
    texts = []

    # d&r text
    for pos, frame in frames:
        rects = text_detect(frame)
        text = text_rec(frame, rects)
        texts.append(text)

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
        similar = string_similar(string1, string2)
        if similar < 0.8 and string1 not in string2:
            flags.append(i+1)
        if i+1 == len(frames)-1 and flags[-1]!=len(frames)-1:
            flags.append(i+1)

    # format & classify text
    res = get_details(flags, duration, frames, texts)
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
    path = 'course_videos/CUC-1206073804'
    video_files = get_all_video(path)

    t1 = datetime.datetime.now()
    print('-'*40)
    print('start at', t1.strftime('%H:%M'))
    i = 0
    for video_file in video_files:
        print("\t{}/{}: {}".format(i, len(video_files), video_file))
        t2 = datetime.datetime.now()
        res = process(video_file)
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
