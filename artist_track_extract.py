from ytmusicapi import YTMusic
import json
import time
import yt_spider
import concurrent.futures
import threading




ytMusic = YTMusic()


def extract(title) :
    data = ytMusic.search(title, filter = "videos")
    print(f"artist_track_extract || track : {data[0]['title']} , artist : {data[0]['artist']}")
    track_data = {
        'track_name' : data[0]['title'],
        'artist' : data[0]['artist']
    }
    return track_data






def get_data(youtube_url) :
    titles = yt_spider.fetch_titles(youtube_url)

    track_data_list = []

    with concurrent.futures.ThreadPoolExecutor() as executor :
        res = executor.map(extract, titles)

        for r in res :
            track_data_list.append(r) 
    
    return track_data_list




