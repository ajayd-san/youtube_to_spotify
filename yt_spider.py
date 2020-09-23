# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
from secrets import yt_api_key
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import json

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
playlist_id = 'PLcucUzinV_SpwO2TGb0k-p7KfD_XtQ82V'

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    api_key = yt_api_key
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = api_key)
    
    get_total_results = youtube.playlistItems().list(
            part="snippet",
            fields = ('pageInfo/totalResults'),
            playlistId = playlist_id,
        )
    response = get_total_results.execute()
    total_results = response['pageInfo']['totalResults']
    if total_results > 100 :
        total_results = 100
    print(total_results)
    nextPageToken = None
    video_title_list = []
    while(True) :
        request = youtube.playlistItems().list(
            part="snippet",
            fields = ('items/snippet/title, nextPageToken, pageInfo/resultsPerPage'),
            playlistId = playlist_id,
            maxResults = 50,
            pageToken = nextPageToken
        )
        response = request.execute()
        if total_results > 50 :
            results_number = 50
            total_results -= 50
        else :
            results_number = total_results
            total_results = 0
            
        for index, i in enumerate(range(results_number)) :
            title = response['items'][i]['snippet']['title']
            print(f'{index}) {title}')
            video_title_list.append(title)
        try :
            nextPageToken = response['nextPageToken']
        except KeyError :
            nextPageToken = None
        if total_results == 0:
            break
    
    return video_title_list


       

if __name__ == "__main__":
    main()