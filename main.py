import os
import sys
import cv2
import json
import datetime
from slicer import VideoSlicerHist
from searcher import get_details
from model import text_rec, text_detect


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

    # Split Video
    slicer = VideoSlicerHist()
    frames = slicer.cut_video(video)
    texts = []

    # detect text & recognize text
    for pos, frame in frames:
        rects = text_detect(frame)
        text = text_rec(frame, rects)
        texts.append(text)

    # format & classify text
    res = get_details(frames, texts)
    for shot in res:
        if shot.type == shot.kShotTypeExample:
            print("{} @ {} -> {}: {}".format(shot.title, shot.start_percent * duration, shot.end_percent * duration,
                                             shot))
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
    i = 0
    for video_file in video_files:
        t2 = datetime.datetime.now()
        res = process(video_file)
        dump(res, video_file[: video_file.rfind('.')] + '.json')
        i += 1
        counter = 0
        for shot in res:
            if shot.type == shot.kShotTypeExample:
                print("exam: {}".format(shot.title))
                counter += 1
        print("time: ", datetime.datetime.now() - t2)
        print("exam count:", counter)
        print("{}/{}: {}".format(i, len(video_files), video_file))

    print("total time: ", datetime.datetime.now() - t1)


if __name__ == '__main__':
    main(sys.argv)
