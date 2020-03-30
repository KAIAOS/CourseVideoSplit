# coding:utf-8
import cv2


class VideoSlicerHist:
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
        cmp_res = []
        for i in range(len(frames) - 1):
            frame1 = frames[i]
            frame2 = frames[i + 1]
            diff = cv2.compareHist(self.calc_hist(frame1), self.calc_hist(frame2), cv2.HISTCMP_BHATTACHARYYA)
            if diff > 0.2:
                res.append((float(i / len(frames)), frame1))
                # print("{}/{}".format(i, len(frames)))
                # cv2.imwrite("/home/henrylee/tmp/{}.png".format(frames), frame1)
        return res

    def calc_hist(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hist = cv2.calcHist([frame], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        return hist
