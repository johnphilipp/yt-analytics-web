from pathlib import Path
import googleapiclient.discovery
import pandas as pd
import numpy as np
import json
import os
import toml

#-----------------------------------------------------------------------

# Return api keys

def _get_youtube_api_key():
    return toml.load(".streamlit/secrets.toml")["youtube_key"]["youtube_key"]

def _get_firebase_api_key():
    return toml.load(".streamlit/secrets.toml")["firebase_key"]

def _get_firebase_storage_path():
    return toml.load(".streamlit/secrets.toml")["firebase_storage_key"]["firebase_storage_key"]

#-----------------------------------------------------------------------

# Return meta data dict

def get_meta(vid):
    # -*- coding: utf-8 -*-

    # Sample Python code for youtube.comments.list
    # See instructions for running these code samples locally:
    # https://developers.google.com/explorer-help/code-samples#python

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Setup
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = _get_youtube_api_key()

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.videos().list(
        id=vid,
        part="snippet,statistics"
    )
    data_all = request.execute()
    
    data = {
        "title": data_all["items"][0]["snippet"]["title"],
        "channel_title": data_all["items"][0]["snippet"]["channelTitle"],
        "thumbnail_url": data_all["items"][0]["snippet"]["thumbnails"]["medium"]["url"],
        "published_at": data_all["items"][0]["snippet"]["publishedAt"],
        "view_count": data_all["items"][0]["statistics"]["viewCount"],
        "like_count": data_all["items"][0]["statistics"]["likeCount"],
        "comment_count": data_all["items"][0]["statistics"]["commentCount"]
    }

    return data


#-----------------------------------------------------------------------

# Return a list with comments data

def _get_comments(vid):
    print("Getting comments")
    # -*- coding: utf-8 -*-

    # Sample Python code for youtube.comments.list
    # See instructions for running these code samples locally:
    # https://developers.google.com/explorer-help/code-samples#python

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Setup
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = _get_youtube_api_key()

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    # Query to retrieve top level comments
    def make_comments_request(vid, pToken):
        request = youtube.commentThreads().list(
            part="snippet, replies",
            videoId=vid,
            maxResults=100, # max 100
            textFormat="plainText",
            order="relevance",
            pageToken=pToken
        )
        return request.execute()

    # Retrieve first page
    comments = []
    pageToken = None # At first API call, pageToken is None
    page = make_comments_request(vid, pageToken)
    comments.append(page)
    pageToken = page.get("nextPageToken")

    # Retrieve successive page(s) if new pageToken
    while pageToken is not None:
        page = make_comments_request(vid, pageToken)
        comments.append(page)
        pageToken = page.get("nextPageToken")
    
    # print(comments)

    return comments

#-----------------------------------------------------------------------

# Return a list with reply data for a list of comments

def _get_replies(comments):
    print("Getting replies")
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Setup
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = _get_youtube_api_key()

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
    
    # Get ids of top level comments which have replies
    ids = []
    for page in comments:
        for i in range(int(len(page["items"]))):
            if page["items"][i].get("replies") != None: 
                ids.append(page["items"][i]["id"])

    # Query to retrieve replies on top level comments
    def make_replies_request(id, pToken):
        request = youtube.comments().list(
            part="snippet",
            parentId=id,
            maxResults=100, # max 100
            pageToken=pToken,
            textFormat="plainText"
        )
        return request.execute()

    replies = []
    for i in range(len(ids)):
        # Retrieve first page
        pageToken = None # At first API call, pageToken is None
        page = make_replies_request(ids[i], pageToken)
        replies.append(page)
        pageToken = page.get("nextPageToken")

        # Retrieve successive page(s) if new pageToken
        while pageToken is not None:
            page = make_replies_request(ids[i], pageToken)
            replies.append(page)
            pageToken = page.get("nextPageToken")
    
    # print(replies)

    return replies   

#-----------------------------------------------------------------------

# Return a df with filtered and stitched comment and reply data for a video id

def get_content_raw(vid):
    print("Getting content")
    # Get comments and replies data for video id
    comments = _get_comments(vid)
    replies = _get_replies(comments)

    # Filter and stitch comments and replies (append comment id and comment content)
    data = []
    for page_c in comments:
        for i in range(int(len(page_c["items"]))):
            comment_id = page_c["items"][i]["id"]
            comment = page_c["items"][i]["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            data.append([comment_id, comment])

            # Fetch replies (append comment id and reply content)
            if page_c["items"][i].get("replies") != None: 
                for page_r in replies:
                    for j in range(int(len(page_r["items"]))):
                        reply_parent_id = page_r["items"][j]["snippet"]["parentId"]
                        reply_id = page_r["items"][j]["id"]
                        reply = page_r["items"][j]["snippet"]["textDisplay"]
                        if reply_parent_id == comment_id:
                            data.append([reply_id, reply])

    # Filter and stitch a df with named cols
    df = pd.DataFrame(np.array(data), columns=["id", "content"])

    return df

#-----------------------------------------------------------------------

# Testing

def main():
    return

if __name__ == '__main__':
    main()
