import toml
from supabase import create_client, Client


def init():
    url: str = toml.load(".streamlit/secrets.toml")["SUPABASE"]["SUPABASE_URL"]
    key: str = toml.load(".streamlit/secrets.toml")["SUPABASE"]["SUPABASE_KEY"]
    return create_client(url, key)


def get_car_id(make, model, trim, year):
    supabase = init()

    def query():
        return supabase.table('CAR').select('car_id').eq('make', make).eq('model', model).eq("trim", trim).eq("year", year).execute()
    data = query()
    if len(data.data) == 0:
        supabase.table("CAR").insert({
            "make": make,
            "model": model,
            "trim": trim,
            "year": year
        }).execute()
        data = query()
        return data.data[0]["car_id"]
    elif len(data.data) == 1:
        return data.data[0]["car_id"]
    elif len(data.data) > 1:
        print("More than one car found. Cars should be unique. Check db")
    else:
        print("Error when trying to retrieve car ({}, {}, {}, {}) from db". format(
            make, model, trim, year))


def insert_meta(video_id, car_id, meta):
    supabase = init()
    supabase.table("META").insert({
        "video_id": video_id,
        "car_id": car_id,
        "title": meta["title"],
        "channel_title": meta["channel_title"],
        "view_count": meta["view_count"],
        "like_count": meta["like_count"],
        "comment_count": meta["comment_count"],
        "thumbnail_url": meta["thumbnail_url"],
        "published_at": meta["published_at"]
    }).execute()
    return "Insert executed"


def insert_content(video_id, content):
    supabase = init()
    content = content.to_dict()
    data = []
    for i in range(0, len(content["id"])):
        data.append(
            {"video_id": video_id, "comment_id": content["id"][i], "content": content["content"][i]})
    supabase.table("CONTENT").insert(data).execute()
    return "Insert executed"


def insert_sentiment(video_id, sentiment):
    supabase = init()
    sentiment = sentiment.to_dict()
    data = []
    for i in range(0, len(sentiment["id"])):
        data.append(
            {"video_id": video_id, "comment_id": sentiment["id"][i], "content": sentiment["content"][i], "sentiment_score": sentiment["sentiment_score"][i]})
    supabase.table("SENTIMENT").insert(data).execute()
    return "Insert executed"
