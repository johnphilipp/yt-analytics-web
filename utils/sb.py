import toml
from supabase import create_client, Client
import pandas as pd


def init():
    url: str = toml.load(".streamlit/secrets.toml")["SUPABASE"]["SUPABASE_URL"]
    key: str = toml.load(".streamlit/secrets.toml")["SUPABASE"]["SUPABASE_KEY"]
    return create_client(url, key)


def get_car_id(make, model, trim, year):
    supabase = init()

    def query():
        return supabase.table("CAR").select("car_id").eq("make", make).eq("model", model).eq("trim", trim).eq("year", year).execute()
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


def get_feature_stats(video_id):
    feature_list = [
        "rim", "steering wheel", "engine", "color", "colour", "carbon", "light", "design", "sound", "interior", "exterior", "mirror", "body",
        "brake", "chassis", "suspension", "gearbox", "navigation", "infotainment", "power", "acceleration", "handling", "range", "battery", "screen"
    ]
    supabase = init()
    data = supabase.table("SENTIMENT").select(
        "content", "sentiment_score").eq("video_id", video_id).execute()
    df = pd.DataFrame(data.data)

    def get_features(df, feature_list):
        # Remove NaNs
        df = df[df["content"].notnull()]

        # Func which returns df of a single feature
        def get_single_feature(df, feature):
            df_single_feature = pd.DataFrame()
            df_single_feature = pd.concat(
                [df_single_feature, df[df["content"].str.lower().str.contains(feature)]], axis=0)
            df_single_feature["feature"] = feature
            return df_single_feature

        # Stitch df_single_feature together into df_features
        df_features = pd.DataFrame()
        for feature in feature_list:
            df_features = pd.concat(
                [df_features, get_single_feature(df, feature)], axis=0)

        return df_features

    df_features = get_features(df, feature_list)

    def get_feature_stats(df_features, feature_list):
        df_feature_stats = []
        for feature in feature_list:
            df_feature_stats.append([feature,
                                    len(df_features[df_features["feature"] == feature]),
                                    df_features[df_features["feature"] == feature]["sentiment_score"].mean()])

        df_feature_stats = pd.DataFrame(df_feature_stats, columns=[
                                        'feature', 'comment_count', 'sentiment_mean'])
        df_feature_stats = df_feature_stats[df_feature_stats['comment_count'] >= 1]
        df_feature_stats = df_feature_stats.sort_values(
            by=["sentiment_mean"], ascending=False)
        df_feature_stats = df_feature_stats.reset_index(drop=True)

        return df_feature_stats

    return get_feature_stats(df_features, feature_list)


def get_makes():
    supabase = init()
    data = supabase.table("CAR").select("make").execute()
    makes = []
    for i in data.data:
        makes.append(i["make"])
    return sorted(set(makes))


def get_models(make):
    supabase = init()
    data = supabase.table("CAR").select("model").eq("make", make).execute()
    models = []
    for i in data.data:
        models.append(i["model"])
    return sorted(set(models))


def get_trim(make, model):
    supabase = init()
    data = supabase.table("CAR").select("trim").eq(
        "make", make).eq("model", model).execute()
    trims = []
    for i in data.data:
        trims.append(i["trim"])
    return sorted(set(trims))


def get_year(make, model, trim):
    supabase = init()
    data = supabase.table("CAR").select("year").eq(
        "make", make).eq("model", model).eq("trim", trim).execute()
    years = []
    for i in data.data:
        years.append(i["year"])
    return sorted(set(years))


def get_video_ids_for_car(car_id):
    supabase = init()
    data = supabase.table("META").select(
        "video_id").eq("car_id", car_id).execute()
    video_ids = []
    for i in data.data:
        video_ids.append(i["video_id"])
    return video_ids


def get_meta(video_id):
    supabase = init()
    data = supabase.table("META").select(
        "*").eq("video_id", video_id).execute()
    return data.data[0]


def get_car_from_video_id(video_id, selection):
    supabase = init()
    data = supabase.table("META").select(
        "car_id").eq("video_id", video_id).execute()
    data = supabase.table("CAR").select(
        selection).eq("car_id", data.data[0]["car_id"]).execute()
    return data.data[0][selection]


def main():
    # print(get_feature_stats("mHhZ9jk-DrU"))
    print(get_makes())
    print(get_models("Polestar"))
    print(get_meta("mHhZ9jk-DrU"))
    print(get_car_from_video_id("mHhZ9jk-DrU"))


if __name__ == '__main__':
    main()
