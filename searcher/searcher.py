from typing import List


class ImageText:#单个文字框
    def __init__(self, text='', x=0, y=0, width=0, height=0, degree=.0):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.degree = degree

    def __str__(self):
        return str(self.__dict__)


class ShotDetail:#一个片段
    kShotTypeUnknown = 0
    kShotTypeExample = 1

    def __init__(self, frame, abstract='', paragraph='', start_time='', end_time='', texts=None, shot_type=0):
        if texts is None:
            texts = list()
        self.frame = frame
        self.abstract = abstract
        self.paragraph = paragraph
        self.audio_paragraph = ''
        self.start_time = start_time
        self.end_time = end_time
        self.texts = texts
        self.type = shot_type

    def __str__(self):
        return "".join([t.text for t in self.texts])


def get_details(flags, duration, frames, texts) -> List[ShotDetail]:
    assert len(frames) == len(texts)
    res = []

    end_percent = .0
    for i in flags:
        start_percent = end_percent
        end_percent, _ = frames[i]
        _, frame = frames[i-1]
        s_time = str(int(start_percent * duration / 60)) + ':' + str(int(start_percent * duration % 60))
        e_time = str(int(end_percent * duration / 60)) + ':' + str(int(end_percent * duration % 60))
        shot_detail = ShotDetail(frame, start_time=s_time, end_time=e_time)
        for text in texts[i-1]:
            img_text = ImageText(text['text'], int(text['cx']), int(text['cy']),
                                 int(text['w']), int(text['h']), text['degree'])
            shot_detail.texts.append(img_text)
            if '例' in text['text'] or '思考题' in text['text']:
                shot_detail.type = ShotDetail.kShotTypeExample

        shot_detail.abstract = get_abstract(shot_detail)
        shot_detail.paragraph = "".join([t.text for t in shot_detail.texts])
        res.append(shot_detail)

    return res


def is_slogan(img_width: int, img_height: int, text: ImageText):
    x_percent = float(text.x) / img_width
    y_percent = float(text.y) / img_height
    return x_percent > 0.75 and y_percent < 0.10


def get_abstract(shot: ShotDetail) -> str:
    res = ''
    height, width = shot.frame.shape[:2]
    if len(shot.texts) < 1:
        return ""
    top_text = shot.texts[-1]
    for text in shot.texts:
        if is_slogan(width, height, text):
            # print("[get_title] drop", text)
            continue
        if top_text.y > text.y:
            top_text = text

    start_y = top_text.y - top_text.height / 2
    end_y = top_text.y + top_text.height / 2

    for text in shot.texts:
        if is_slogan(width, height, text):
            continue
        if start_y < text.y < end_y:
            res += text.text

    return res
