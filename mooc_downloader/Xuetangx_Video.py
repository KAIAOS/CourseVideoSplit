import requests
import json
import subprocess
import os

class XuetangxVideo():


    def __init__(self):
        self.resource_info = dict()
        self.url = 'https://next.xuetangx.com/api/v1/lms/learn/course/chapter?cid=1265406&sign=CAU08091000589'
        self.cid = '1265406'
        self.sign = 'CAU08091000589'
        self.cookie = 'login_type=P; csrftoken=izELgVzmEUeKRbbht5NRxJQe95Ff12zW; sessionid=fpchaz5cr4q2xc03c2l2zp1f357l4t1c; k=28624931'
        self.csrftoken = 'izELgVzmEUeKRbbht5NRxJQe95Ff12zW'

    def download_video(self):
        dirname = '../course_videos/CAU08091000589'
        jsonname = 'CAU08091000589.json'
        jsonpath = os.path.join(dirname, jsonname)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(jsonpath, 'r') as f:
            self.resource_info = json.load(f)

        aira2_cmd = 'aria2c.exe {url:} -o {filename:}'
        for chapter in self.resource_info['course_chapter']:
            section_leaf_list = chapter['section_leaf_list']
            for leaf in section_leaf_list:
                if 'leaf_list' not in leaf.keys():
                    continue
                leaf_list = leaf['leaf_list']
                for video in leaf_list:
                    if video['leaf_type'] != 0:
                        continue
                    videoname = video['save_name'] + '.mp4'
                    videopath = os.path.join(dirname, videoname)
                    url = video['url']
                    cmd = aira2_cmd.format(url=url, filename=videopath)
                    subprocess.run(cmd, shell=False, stdout=subprocess.PIPE)
                    print('download:', videoname)

    def crawl_video(self):
        self._get_course_chapter()
        for chapter in self.resource_info['course_chapter']:
            section_leaf_list = chapter['section_leaf_list']
            prefix1 = chapter['name'].split(' ')[0]
            for leaf in section_leaf_list:
                if 'leaf_list' not in leaf.keys():
                    continue
                leaf_list = leaf['leaf_list']
                prefix2 = leaf['name'].split(' ')[0]
                for video in leaf_list:
                    if video['leaf_type'] != 0:
                        continue
                    del video['is_locked']
                    del video['start_time']
                    del video['chapter_id']
                    del video['section_id']
                    del video['is_show']
                    del video['end_time']
                    del video['score_deadline']
                    del video['is_assessed']
                    del video['leafinfo_id']
                    video['url'] = self._get_video_url(video['id'])
                    video['save_name'] = prefix1 + prefix2 + video['name']

        dirname = '../course_videos/CAU08091000589'
        filename = 'CAU08091000589.json'
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        filepath = os.path.join(dirname, filename)
        with open(filepath, 'w') as f:
            json_str = json.dumps(self.resource_info)
            f.write(json_str)

    def _get_course_chapter(self):
        url = self.url
        payload = {}
        headers = {
            'cookie': self.cookie,
            'xtbz': 'xt'
        }

        r = requests.request("GET", url, headers=headers, data=payload)
        d = r.json()
        self.resource_info['course_chapter'] = d['data']['course_chapter']
        self.resource_info['course_name'] = d['data']['course_name']

    def _get_video_url(self, id):
        url = "https://next.xuetangx.com/api/v1/lms/learn/leaf_info/"+ self.cid + "/" + str(id) + "/?sign=" + self.sign
        payload = {}
        headers = {
            'cookie': self.cookie,
            'xtbz': 'xt'
        }
        r = requests.request("GET", url, headers=headers, data=payload)
        d = r.json()
        ccid = d['data']['content_info']['media']['ccid']

        url = "https://next.xuetangx.com/api/v1/lms/service/playurl/" + str(ccid)+ "/?appid=10000"
        r = requests.request("GET", url)
        d = r.json()
        return d['data']['sources']['quality10'][0]

    def _get_product_id(self):

        url = "https://next.xuetangx.com/api/v1/lms/product/sku_pay_detail/?cid=1265406&sign=CAU08091000589"
        payload = {
        }
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
        }
        r = requests.request("GET", url, headers=headers, data=payload)
        d = r.json()

        return d['data']['product_id'], d['data']['sku_info'][0]['sku_id']


    def _join_class(self, product_id, sku_id):
        url = "https://next.xuetangx.com/api/v1/lms/order/entries_free_sku/"+ str(product_id) + "/?sid=" + str(sku_id)
        payload = {}
        headers = {
            'cookie': self.cookie,
            'xtbz': 'xt',
            'x-csrftoken': self.csrftoken
        }

        r = requests.request("POST", url, headers=headers, data=payload)
        d = r.json()
        print(d)

if __name__ == '__main__':
    xuetang = XuetangxVideo()
    xuetang.crawl_video()
    xuetang.download_video()