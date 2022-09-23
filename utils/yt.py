import googleapiclient.discovery
import pandas as pd
import numpy as np
import os
import toml


def _get_youtube_api_key():
    """
    Return API key
    """
    return toml.load(".streamlit/secrets.toml")["youtube_key"]["youtube_key"]


# -----------------------------------------------------------------------

# Return meta data dict

def get_meta(vid):
    """
    Return YouTube meta data dict
    """
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = _get_youtube_api_key()

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

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


def _get_comments(vid):
    """
    Return a list with comments data
    """
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = _get_youtube_api_key()

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    def make_comments_request(vid, pToken):
        """
        Return top level comments
        """
        request = youtube.commentThreads().list(
            part="snippet, replies",
            videoId=vid,
            maxResults=100,  # max 100
            textFormat="plainText",
            order="relevance",
            pageToken=pToken
        )
        return request.execute()

    comments = []
    pageToken = None
    page = make_comments_request(vid, pageToken)
    comments.append(page)
    pageToken = page.get("nextPageToken")

    while pageToken is not None:
        page = make_comments_request(vid, pageToken)
        comments.append(page)
        pageToken = page.get("nextPageToken")

    return comments


def _get_replies(comments):
    """
    Return a list with reply data for a list of comments
    """
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = _get_youtube_api_key()

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    ids = []
    for page in comments:
        for i in range(int(len(page["items"]))):
            if page["items"][i].get("replies") != None:
                ids.append(page["items"][i]["id"])

    def make_replies_request(id, pToken):
        request = youtube.comments().list(
            part="snippet",
            parentId=id,
            maxResults=100,
            pageToken=pToken,
            textFormat="plainText"
        )
        return request.execute()

    replies = []
    for i in range(len(ids)):
        pageToken = None
        page = make_replies_request(ids[i], pageToken)
        replies.append(page)
        pageToken = page.get("nextPageToken")

        while pageToken is not None:
            page = make_replies_request(ids[i], pageToken)
            replies.append(page)
            pageToken = page.get("nextPageToken")

    return replies


def get_content_raw(vid):
    """
    Return a df with filtered and stitched comment and reply data for a video id
    """
    comments = _get_comments(vid)
    replies = _get_replies(comments)

    data = []
    for page_c in comments:
        for i in range(int(len(page_c["items"]))):
            comment_id = page_c["items"][i]["id"]
            comment = page_c["items"][i]["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            data.append([comment_id, comment])

            if page_c["items"][i].get("replies") != None:
                for page_r in replies:
                    for j in range(int(len(page_r["items"]))):
                        reply_parent_id = page_r["items"][j]["snippet"]["parentId"]
                        reply_id = page_r["items"][j]["id"]
                        reply = page_r["items"][j]["snippet"]["textDisplay"]
                        if reply_parent_id == comment_id:
                            data.append([reply_id, reply])

    df = pd.DataFrame(np.array(data), columns=["id", "content"])

    return df
