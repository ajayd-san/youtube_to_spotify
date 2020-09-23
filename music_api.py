from ytmusicapi import YTMusic
import json
import time
import yt_spider
import concurrent.futures
import threading
titles = yt_spider.main()
start = time.time()


ytMusic = YTMusic()
track_data = {}
counter = 1

def extract(title) :
    data = ytMusic.search(title, filter = "videos")
    print(f"track : {data[0]['title']} , artist : {data[0]['artist']}")
    # track_data[counter] = {
    #     'track_name' : data[0]['title'],
    #     'artist' : data[0]['artist']
    # }
    # counter+=1




threads = []


with concurrent.futures.ThreadPoolExecutor() as executor :
    res = executor.map(extract, titles)

# print(track_data)

print(f"time taken = {time.time() - start}")