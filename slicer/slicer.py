# coding:utf-8
import cv2

class VideoSlicer:
    #sampling by 5s
    def cut_video(self, video: cv2.VideoCapture) -> list:
        frames = []
        total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        rate = int(video.get(cv2.CAP_PROP_FPS))
        step = 5
        for i in range(1, total, rate * step):
            video.set(cv2.CAP_PROP_POS_FRAMES, i)
            _, frame = video.read()
            frames.append(frame)

        res = []
        for i in range(len(frames)):
            res.append((float(i / len(frames)), frames[i]))

        return res

    #sampling by audio
    def cut_video_by_audio(self, video: cv2.VideoCapture, audio) -> list:
        frames = []
        total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        rate = int(video.get(cv2.CAP_PROP_FPS))
        step = 5
        for i in range(1, total, rate * step):
            video.set(cv2.CAP_PROP_POS_FRAMES, i)
            _, frame = video.read()
            frames.append(frame)

        res = []
        res.append((float(0 / len(frames)), frames[0]))
        begin = 0
        end = 5
        for i in range(1,len(frames)):
            counter = self.count_breaks(begin, end, audio)
            if counter >= 3:
                res.append((float(i / len(frames)), frames[i]))
                begin = end
            else:
                end = end + 5
        return res

    def count_breaks(self, begin, end, audio):
        samplerate = 16000
        counter = 0
        for i in range(begin*samplerate, end*samplerate, samplerate):
            if abs(audio[i]) < 500:
                counter += 1
        return counter

