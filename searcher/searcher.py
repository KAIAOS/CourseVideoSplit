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

    def __init__(self, frame, title='', start_percent=.0, end_percent=.0, texts=None, shot_type=0):
        if texts is None:
            texts = list()
        self.frame = frame# end_percent对应frame
        self.title = title
        self.start_percent = start_percent
        self.end_percent = end_percent
        self.texts = texts
        self.type = shot_type

    def __str__(self):
        return "".join([t.text for t in self.texts])


def get_details(frames, texts) -> List[ShotDetail]:
    assert len(frames) == len(texts)
    res = []
    arr_len = len(frames)

    start_percent = .0
    end_percent = .0
    for i in range(arr_len):
        start_percent = end_percent
        end_percent, frame = frames[i]

        shot_detail = ShotDetail(frame, start_percent=start_percent, end_percent=end_percent)
        for text in texts[i]:
            img_text = ImageText(text['text'], int(text['cx']), int(text['cy']),
                                 int(text['w']), int(text['h']), text['degree'])
            shot_detail.texts.append(img_text)
            if '例' in text['text'] or '思考题' in text['text']:
                shot_detail.type = ShotDetail.kShotTypeExample

        shot_detail.title = get_title(shot_detail)
        res.append(shot_detail)

    return res


def is_slogan(img_width: int, img_height: int, text: ImageText):
    x_percent = float(text.x) / img_width
    y_percent = float(text.y) / img_height
    return x_percent > 0.75 and y_percent < 0.10


def get_title(shot: ShotDetail) -> str:
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
