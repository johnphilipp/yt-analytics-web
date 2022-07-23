from pathlib import Path
import googleapiclient.discovery
import pandas as pd
import numpy as np
import json
import os
import sys
import toml

#-----------------------------------------------------------------------

# Return api keys

def _get_youtube_api_key():
    # main_dir = os.path.dirname(__file__)
    # key_dir = os.path.join(main_dir, "../keys/youtube_key.txt")
    # with open(key_dir) as f:
    #     key = f.readline()
    # return key
    return toml.load(".streamlit/secrets.toml")["youtube_key"]["youtube_key"]

def _get_firebase_api_key():
    return toml.load(".streamlit/secrets.toml")["firebase_key"]

def _get_firebase_storage_path():
    return toml.load(".streamlit/secrets.toml")["firebase_storage_key"]["firebase_storage_key"]

#-----------------------------------------------------------------------

# Return a list with comments data

def _get_comments(dir, vid):
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
    
    # Write to json
    with open(dir + "/comments.json", "w") as f:
        json.dump(comments, f)

    return comments

#-----------------------------------------------------------------------

# Return a list with reply data for a list of comments

def _get_replies(dir, comments):
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

    # Write to json
    with open(dir + "/replies.json", "w") as f:
        json.dump(replies, f)
    
    return replies   

#-----------------------------------------------------------------------

# Return a df with filtered and stitched comment and reply data for a 
# video id

def get_content(dir, url):
    # Get video id from video url
    if "youtu.be" in url:
        # e.g., https://youtu.be/kbulCM90w8w
        vid = url.rsplit('/', 1)[-1]
        if "?" in url:
            # e.g., https://youtu.be/kbulCM90w8w?t=269
            vid = vid.split("?", 1)[0]
    elif "youtube.com" in url:
        # e.g., https://www.youtube.com/watch?v=kbulCM90w8w
        vid = url.rsplit('v=', 1)[-1]
        if "&" in url:
            # e.g., https://www.youtube.com/watch?v=kbulCM90w8w&t=3s 
            vid = vid.split("&", 1)[0]
    else:
        print("URL invalid")
        sys.exit()
    print(vid)

    # Get comments and replies data for video id
    comments = _get_comments(dir, vid)
    replies = _get_replies(dir, comments)

    # Filter and stitch comments and replies
    data = []
    # Filter and stitch comments (append comment id and comment content)
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

    # Write df
    df.to_csv(dir + "/content.csv")  

    return df

#-----------------------------------------------------------------------

# Return 

# def get_thumbnail(dir, vid):
def get_thumbnail(vid):
    print("\n" + vid + "\n")
    import urllib.request
    img_url = "http://img.youtube.com/vi/" + vid + "/mqdefault.jpg"
    save_path = "data/" + vid
    Path(save_path).mkdir(parents=True, exist_ok=True)
    img = urllib.request.urlretrieve(img_url, save_path + "/thumbnail.jpg")

    from firebase_admin import credentials, initialize_app, storage
    # Init firebase with your credentials
    cred = credentials.Certificate(_get_firebase_api_key())
    initialize_app(cred, {'storageBucket': _get_firebase_storage_path()})

    # Put your local file path 
    fileName = "data/" + vid + "/thumbnail.jpg"
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

    # Opt : if you want to make public access from the URL
    blob.make_public()

    return blob.public_url

    # from PIL import Image
    # import requests
    # from io import BytesIO
    # img_url = "http://img.youtube.com/vi/" + vid + "/mqdefault.jpg"
    # response = requests.get(img_url)
    # img = Image.open(BytesIO(response.content))
    # print(img)

#-----------------------------------------------------------------------

# Testing

def main():
    vid = "cjdAGs7fEpc"
    print(get_thumbnail(vid))

if __name__ == '__main__':
    main()
