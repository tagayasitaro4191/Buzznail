#coding: utf-8
#----- 標準ライブラリ -----#
import requests
import json
import os
import random
import string
from time import sleep
import re
import shutil
import json
import datetime

#----- 専用ライブラリ -----#
import numpy as np
from apiclient.discovery import build
import pandas as pd
from tqdm import tqdm

#----- 自作モジュール -----#
# None

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
    #APIkeyを設定
    #API_KEY = "APIkey"


    youtube_API = build(
        'youtube',
        'v3',
        developerKey=API_KEY
    )
    return youtube_API

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
        "channel_ID": channel_ID,
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


if __name__ == "__main__":
    youtube_API = get_youtube_API()
    
    day = random.randint(1, 31)

    start_term = datetime.datetime(2022, 10, day, 0, 0).isoformat() + 'Z'
    end_term = datetime.datetime(2022, 10, day, 23, 59).isoformat() + 'Z'
    
    channel, video_result = get_term_videos(youtube_API, '20', start_term, end_term, n=12)
