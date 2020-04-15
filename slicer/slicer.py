# coding:utf-8
import cv2

class VideoSlicer:
    #sampling by hist
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
        res.append((float(0 / len(frames)), frames[0]))
        flag = 0
        for i in range(1, len(frames)):
            frame = frames[i]
            flag_framg = frames[flag]
            diff = cv2.compareHist(self.calc_hist(flag_framg), self.calc_hist(frame), cv2.HISTCMP_BHATTACHARYYA)
            if diff > 0.09:
                flag = i
                res.append((float(i / len(frames)), frame))
                # name = 'test_imgs/' + str(i) + '.png'
                # cv2.imwrite(name, frame)
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

    def calc_hist(self, frame):
        hist = cv2.calcHist([frame], [0], None, [256], [0, 255])
        return hist
