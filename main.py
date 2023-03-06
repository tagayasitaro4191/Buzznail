#coding: utf-8
#----- 標準ライブラリ -----#
import requests
import json
import os
import random
import string
from time import sleep
import re

#----- 専用ライブラリ -----#
from apiclient.discovery import build
import shutil
import torch
import torch.nn.functional as F
from flask import Flask, render_template, request, url_for, redirect
import PIL.Image as Image
import numpy as np
import cv2
import pathlib
import datetime
from operator import itemgetter
from io import BytesIO
import base64
import tempfile

#----- 自作モジュール -----#
from youtube_inference.inference import AI_model

app = Flask(__name__)
model = AI_model()

IMG_EXTENSIONS = ['.jpg', '.jpeg', '.png']
VIDEO_EXTENSIONS = ['.MOV', '.MP4']
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

man = 10 ** 4
class_section = [0, 100, 500, 1000, 5000, 1 * man, 5 * man, 10 * man, 50 * man, 100 * man, 500 * man, 1000 * man, np.inf]
class_section = ["0", "100", "500", "1000", "5000", "1万", "5万", "10万", "50万", "100万", "500万", "1000万", "1億"]



TAG_input = {
    "映画とアニメ": "1" ,
    "自動車と乗り物": "2" ,
    "音楽":"10",
    "ペットと動物":"15",
    "スポーツ":"17",
    "旅行とイベント":"19",
    "ゲーム":"20",
    "ブログ":"22",
    "コメディー":"23",
    "エンターテイメント":"24",
    "ニュースと政治":"25",
    "ハウツーとスタイル":"26",
    "教育":"27",
    "科学と技術":"28",
    "非営利団体と社会活動":"29",
    "映画":"30",
    "アニメ":"31",
    "アクション/アドベンチャー":"32",
    "クラシック":"33",
    "コメディー":"34",
    "ドキュメンタリー":"35",
    "ドラマ":"36",
    "家族向け":"37",
    "海外":"38",
    "ホラー":"39",
    "SF/ファンタジー":"40",
    "サスペンス":"41",
    "短編":"42",
    "番組":"43",
    "予告編":"44"
}

TAG = {
    "1": "映画とアニメ",
    "2": "自動車と乗り物",
    "10": "音楽",
    "15": "ペットと動物",
    "17": "スポーツ",
    "19": "旅行とイベント",
    "20": "ゲーム",
    "22": "ブログ",
    "23": "コメディー",
    "24": "エンターテイメント",
    "25": "ニュースと政治",
    "26": "ハウツーとスタイル",
    "27": "教育",
    "28": "科学と技術",
    "29": "非営利団体と社会活動",
    "30": "映画",
    "31": "アニメ",
    "32": "アクション/アドベンチャー",
    "33": "クラシック",
    "34": "コメディー",
    "35": "ドキュメンタリー",
    "36": "ドラマ",
    "37": "家族向け",
    "38": "海外",
    "39": "ホラー",
    "40": "SF/ファンタジー",
    "41": "サスペンス",
    "42": "短編",
    "43": "番組",
    "44": "予告編",
}


def get_youtube_API():
    # youtubeのAPIkey
    #API_KEY = 

    youtube_API = build(
        'youtube',
        'v3',
        developerKey=API_KEY
    )

    return youtube_API

def get_info(dicts, key):
    if dicts.get(key) is not None:
        return dicts[key]
    else:
        return None

def get_term_videos(API, category, start_time, end_time, n=12):
    #動画検索
    search_responses = API.search().list(
        videoCategoryId=category,
        publishedAfter=start_time,
        publishedBefore=end_time,
        part='id',
        type='video',
        order="relevance",
        regionCode="jp",
        maxResults=n,# 5~50まで
        ).execute()

    #channel id: channel name
    channel = {}
    channel_ID = []
    thumbnail_url = []
    thumbnail_H = []
    thumbnail_W = []
    title = []
    main_tag = []
    sub_tags = []
    view_count = []
    line_count = []
    comment_count = []
    submission_time = []

    for search_response in search_responses['items']:
        video_id = search_response["id"]["videoId"]
        videos_response = API.videos().list(
            part='snippet,statistics',
            id=f'{video_id}'
            ).execute()
        videos_snippet = videos_response["items"][0]['snippet']
        videos_statistics = videos_response["items"][0]['statistics']

        #チャンネルID,名前保存
        channel[videos_snippet["channelId"]] = videos_snippet["channelTitle"]
        channel_ID.append(get_info(videos_snippet, "channelId"))
        
        if videos_snippet["thumbnails"].get("standard") is not None:
            img_type = "standard"
        elif videos_snippet["thumbnails"].get('high') is not None:
            img_type = "high"
        #サムネURL保存
        thumbnail_url.append(videos_snippet["thumbnails"][img_type]["url"])
        #サムネHW保存
        thumbnail_H.append(videos_snippet["thumbnails"][img_type]["height"])
        thumbnail_W.append(videos_snippet["thumbnails"][img_type]["width"])
        #タイトル保存
        title.append(videos_snippet["title"])
        #メインタグ保存
        main_tag.append(TAG[videos_snippet["categoryId"]])
        #サブのタグ保存
        sub_tags.append(get_info(videos_snippet, "tags"))
        #再生数保存
        view_count.append(get_info(videos_statistics, "viewCount"))
        #高評価数保存
        line_count.append(get_info(videos_statistics, "likeCount"))
        #コメント数保存
        comment_count.append(get_info(videos_statistics, "commentCount"))
        #投稿時間
        submission_time.append(get_info(videos_snippet, "publishedAt"))

    video_dict = {
        "channel_name": [v for v in channel.values()],
        "thumbnail_url": thumbnail_url,
        "thumbnail_H": thumbnail_H,
        "thumbnail_W": thumbnail_W,
        "title": title,
        "main_tag": main_tag,
        "sub_tags": sub_tags,
        "view_count": view_count,
        "line_count": line_count,
        "comment_count": comment_count,
        "submission_time": submission_time
    }
    return channel, video_dict

def rmdir(path):
    if os.path.exists(path):
        os.remove(path)

def imread_web(url):
    # 画像をリクエストする
    res = requests.get(url)
    img = None
    # Tempfileを作成して即読み込む
    with tempfile.NamedTemporaryFile(dir='./') as fp:
        fp.write(res.content)
        fp.file.seek(0)
        img = cv2.imread(fp.name)
    return img

@app.route('/')
def index():
	return render_template('index_input.html')


@app.route('/get_input_data', methods=['POST'])
def get_input_data():
    print(request.form)
    print(request.files)
    tagname = request.form.get('category')

    youtube_API = get_youtube_API()

    day = random.randint(1, 30)
    
    # データをとってくる日付を指定
    start_term = datetime.datetime(2022, 10, day, 0, 0).isoformat() + 'Z'
    end_term = datetime.datetime(2022, 10, day, 23, 59).isoformat() + 'Z'
    
    channel, video_result = get_term_videos(youtube_API, '20', start_term, end_term, n=12)

    if request.form.get('file_btn') == "true":

        fs = request.files['img_video_file']
        suffix = pathlib.Path(fs.filename).suffix

        if True:
            stream = request.files['img_video_file'].stream

            #with open(filename,'rb') as f: img_bytes = f.read()

            img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
            img = cv2.imdecode(img_array, flags=cv2.IMREAD_COLOR)

            cv2.imwrite('static/preview.png', img)

            value, index = model(img)

            start_output = itemgetter(*index)(class_section)
            end_output = itemgetter(*(index + 1))(class_section)
            
            return render_template('index_output.html', preview='static/preview.png', predicted_view_counts1=f"{start_output}", predicted_view_counts2=f"{end_output}",
                    thumbnail=video_result['thumbnail_url'], title=video_result["title"], 
                    view_counts=video_result["view_count"], channel=video_result["channel_name"])

        elif suffix in VIDEO_EXTENSIONS:
            file = request.files['image_video_file']

            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            cap = cv2.VideoCapture(UPLOAD_FOLDER + "/" + filename)
            # frame数取得
            total_frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            # frameの幅取得
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            # frameの高さ取得
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            if total_frame_num <= 1000:
                # input初期化
                input_frames = np.empty((total_frame_num, height, width, 3))
                for input_idx in range(total_frame_num):
                    # .read()するとフレームが1進む
                    ret, frame = cap.read()
                    input_frames[input_idx] = np.expand_dims(frame, 0)

            if total_frame_num > 1000:
                input_frames = np.empty((1000, height, width, 3))

                inc = total_frame_num / 1000

                frame_list = []

                frame_idx = 0
                input_idx = 0

                while frame_idx < total_frame_num:
                    # フレーム指定
                    frame_list.append(round(frame_idx))
                    cap.set(cv2.CAP_PROP_POS_FRAMES, round(frame_idx))
                    ret, frame = cap.read()
                    input_frames[input_idx] = np.expand_dims(frame, 0)

                    frame_idx += inc
                    input_idx += 1

            value, index = model(input_frames)

            value = F.softmax(value, dim=1)

            output = value + index

            sorted_label, sorted_index = torch.sort(int(output), descending=True)

            label_top5 = sorted_label[:5]
            index_top5 = sorted_index[:5]

            start_output = itemgetter(*label_top5)(class_section)
            end_output = itemgetter(*(label_top5))(class_section)        

            recommend_list = []

            result_path = "best_frame_"

            for i in index_top5:
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()

                cv2.imwrite(result_path, frame)
                recommend_list.append()

            rmdir(UPLOAD_FOLDER + "/" + filename)

            cap.release()
            cv2.destroyAllWindows()

            return render_template('index_output.html', predicted_view_counts1=f"{start_output}", predicted_view_counts2=f"{end_output}", reccomend_frame=recommend_list,
                    thumbnail=video_result['thumbnail_url'], title=video_result["title"], 
                    view_counts=video_result["view_count"], channel=video_result["channel_name"])

    else:
        
        video_url = request.form.get('youtube_url')

        videoId = video_url.replace('https://www.youtube.com/watch?v=', '')

        url1 = 'https://img.youtube.com/vi/'

        url2  ='/sddefault.jpg'

        url = url1 + videoId + url2

        # 画像をリクエストする
        res = requests.get(url)
        img = None

        # Tempfileを作成して即読み込む
        with tempfile.NamedTemporaryFile(dir='./') as fp:
            fp.write(res.content)
            fp.file.seek(0)
            img = cv2.imread(fp.name)

        value, index = model(img)

        start_output = itemgetter(*index)(class_section)

        end_output = itemgetter(*(index+1))(class_section)

        a = render_template('index_output.html', preview=url, predicted_view_counts1=f"{start_output}", predicted_view_counts2=f"{end_output}",
                thumbnail=video_result['thumbnail_url'], title=video_result["title"], 
                view_counts=video_result["view_count"], channel=video_result["channel_name"])

        return render_template('index_output.html', preview=url, predicted_view_counts1=f"{start_output}", predicted_view_counts2=f"{end_output}",
                thumbnail=video_result['thumbnail_url'], title=video_result["title"], 
                view_counts=video_result["view_count"], channel=video_result["channel_name"])

if __name__ == "__main__":
	app.run(port=2000, debug=True)