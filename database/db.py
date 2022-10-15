import toml
from supabase import create_client, Client
import pandas as pd


def init():
    url: str = toml.load(".streamlit/secrets.toml")["SUPABASE"]["SUPABASE_URL"]
    key: str = toml.load(".streamlit/secrets.toml")["SUPABASE"]["SUPABASE_KEY"]
    return create_client(url, key)


def get_car_id(make, model, trim="", year="", form_previews=None):
    supabase = init()

    def query():
        if form_previews is None:
            if (make != "") and (model != "") and (trim != "") and (year != ""):
                return supabase.table("CAR").select("car_id").eq("make", make).eq("model", model).eq("trim", trim).eq("year", year).execute()
            elif (make != "") and (model != "") and (trim != ""):
                return supabase.table("CAR").select("car_id").eq("make", make).eq("model", model).eq("trim", trim).execute()
            elif (make != "") and (model != ""):
                return supabase.table("CAR").select("car_id").eq("make", make).eq("model", model).execute()
            elif (make != ""):
                return supabase.table("CAR").select("car_id").eq("make", make).execute()
        else:
            if (make != "" and make != form_previews["make"]) and (model != "" and model != form_previews["model"]) and (trim != "" and trim != form_previews["trim"]) and (year != "" and year != form_previews["year"]):
                return supabase.table("CAR").select("car_id").eq("make", make).eq("model", model).eq("trim", trim).eq("year", year).execute()
            elif (make != "" and make != form_previews["make"]) and (model != "" and model != form_previews["model"]) and (trim != "" and trim != form_previews["trim"]):
                return supabase.table("CAR").select("car_id").eq("make", make).eq("model", model).eq("trim", trim).execute()
            elif (make != "" and make != form_previews["make"]) and (model != "" and model != form_previews["model"]):
                return supabase.table("CAR").select("car_id").eq("make", make).eq("model", model).execute()
            elif (make != "" and make != form_previews["make"]):
                return supabase.table("CAR").select("car_id").eq("make", make).execute()
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
        car_ids = []
        for i in data.data:
            car_ids.append(i["car_id"])
        return car_ids
    else:
        print("Error when trying to retrieve car ({}, {}, {}, {}) from db". format(
            make, model, trim, year))


def get_car_id_from_make_model(make, model):
    supabase = init()

    data = supabase.table("CAR").select("car_id").eq(
        "make", make).eq("model", model).execute()
    if len(data.data) == 0:
        print("Warning: '{} {}' not found in db".format(make, model))
        return 0
    elif len(data.data) == 1:
        return [data.data[0]["car_id"]]
    elif len(data.data) > 1:
        car_ids = []
        for i in data.data:
            car_ids.append(i["car_id"])
        return car_ids
    else:
        print("Error when trying to retrieve car ({}, {}) from db". format(
            make, model))


def get_num_comments(video_id):
    supabase = init()
    return supabase.table("CONTENT").select("video_id", count="exact").eq("video_id", video_id).execute().count


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


def insert_content(video_id, car_id, content):
    supabase = init()
    content = content.to_dict()
    data = []
    for i in range(0, len(content["id"])):
        data.append(
            {"video_id": video_id, "car_id": car_id, "comment_id": content["id"][i], "content": content["content"][i]})
    supabase.table("CONTENT").insert(data).execute()
    return "Insert executed"


def insert_sentiment(video_id, car_id, sentiment):
    supabase = init()
    sentiment = sentiment.to_dict()
    data = []
    for i in range(0, len(sentiment["id"])):
        data.append(
            {"video_id": video_id, "car_id": car_id, "comment_id": sentiment["id"][i], "content": sentiment["content"][i], "sentiment_score": sentiment["sentiment_score"][i]})
    supabase.table("SENTIMENT").insert(data).execute()
    return "Insert executed"


def get_content(video_id):
    supabase = init()
    data = supabase.table("SENTIMENT").select(
        "content").eq("video_id", video_id).execute()
    df = []
    for i in data.data:
        df.append(i["content"])
    return df


def get_content_and_sentiment_for_car_id(car_id):
    supabase = init()
    data = supabase.table("SENTIMENT").select(
        "content", "sentiment_score").eq("car_id", car_id).execute()
    df = []
    for i in data.data:
        df.append([i["content"], i["sentiment_score"]])
    return df


def get_feature_stats_for_make_model(make, model):
    feature_list = [
        "rim", "steering wheel", "engine", "color", "colour", "carbon", "light", "design", "sound", "interior", "exterior", "mirror", "body",
        "brake", "chassis", "suspension", "gearbox", "navigation", "infotainment", "power", "acceleration", "handling", "range", "battery", "screen"
    ]
    supabase = init()
    data = supabase.table("SENTIMENT").select(
        "content", "sentiment_score").eq("car_id", car_id).execute()
    df = pd.DataFrame(data.data)

    def _get_features(df, feature_list):
        def _get_single_feature(df, feature):
            df_single_feature = pd.DataFrame()
            df_single_feature = pd.concat(
                [df_single_feature, df[df["content"].str.lower().str.contains(feature)]], axis=0)
            df_single_feature["feature"] = feature
            return df_single_feature

        df = df[df["content"].notnull()]
        df_features = pd.DataFrame()
        for feature in feature_list:
            df_features = pd.concat(
                [df_features, _get_single_feature(df, feature)], axis=0)

        return df_features

    df_features = _get_features(df, feature_list)

    def _get_feature_stats(df_features, feature_list):
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

    return _get_feature_stats(df_features, feature_list)


def get_feature_stats_for_cars(cars):
    def _get_features(df, feature_list):
        def _get_single_feature(df, feature):
            df_single_feature = pd.DataFrame()
            df_single_feature = pd.concat(
                [df_single_feature, df[df["content"].str.lower().str.contains(feature)]], axis=0)
            df_single_feature["feature"] = feature
            return df_single_feature

        df = df[df["content"].notnull()]
        df_features = pd.DataFrame()
        for feature in feature_list:
            df_features = pd.concat(
                [df_features, _get_single_feature(df, feature)], axis=0)

        return df_features

    def _get_feature_stats(make, model, df_features, feature_list):
        df_feature_stats = []
        for feature in feature_list:
            df_feature_stats.append([make,
                                     model,
                                     feature,
                                    len(df_features[df_features["feature"] == feature]),
                                    df_features[df_features["feature"] == feature]["sentiment_score"].mean()])

        df_feature_stats = pd.DataFrame(df_feature_stats, columns=[
                                        'make', 'model', 'feature', 'comment_count', 'sentiment_mean'])
        df_feature_stats = df_feature_stats[df_feature_stats['comment_count'] >= 1]
        df_feature_stats = df_feature_stats.sort_values(
            by=["sentiment_mean"], ascending=False)
        df_feature_stats = df_feature_stats.reset_index(drop=True)

        return df_feature_stats

    feature_list = [
        "rim", "steering wheel", "engine", "color", "colour", "carbon", "light", "design", "sound", "interior", "exterior", "mirror", "body",
        "brake", "chassis", "suspension", "gearbox", "navigation", "infotainment", "power", "acceleration", "handling", "range", "battery", "screen"
    ]

    supabase = init()
    df = pd.DataFrame(
        columns=["make", "model", "car_id", "content", "sentiment_score"])

    df_features = pd.DataFrame(
        columns=["make", "model", "car_id", "content", "sentiment_score", "feature"])

    df_feature_stats = pd.DataFrame(
        columns=["make", "model", "feature", "comment_count", "sentiment_mean"])

    if isinstance(cars, int):
        make = get_make_from_car_id(cars)
        model = get_model_from_car_id(cars)
        data = supabase.table("SENTIMENT").select(
            "car_id", "content", "sentiment_score").eq("car_id", cars).execute()
        data = pd.DataFrame(data.data)
        df = pd.concat([df, data]).sort_values(by=["car_id"])
        df['make'] = df['make'].fillna(make)
        df['model'] = df['model'].fillna(model)

        df_features = pd.concat([df_features, _get_features(
            df, feature_list)]).sort_values(by=["car_id"])

        df_feature_stats = pd.concat([df_feature_stats, _get_feature_stats(
            make, model, df_features, feature_list)]).sort_values(by=["make", "model"])

        df_feature_stats['car'] = df_feature_stats[["make", "model"]].apply(
            lambda row: ' '.join(row.values.astype(str)), axis=1)
        df.drop(columns=['make', 'model'], inplace=True)
        df_feature_stats = df_feature_stats.sort_values(by=["feature"])
    else:
        for make in cars.keys():
            for model in cars[make].keys():
                for car_id in cars[make][model].keys():
                    data = supabase.table("SENTIMENT").select(
                        "car_id", "content", "sentiment_score").eq("car_id", car_id).execute()
                    data = pd.DataFrame(data.data)
                    df = pd.concat([df, data]).sort_values(by=["car_id"])
                df['make'] = df['make'].fillna(make)
                df['model'] = df['model'].fillna(model)

                df_features = pd.concat([df_features, _get_features(
                    df, feature_list)]).sort_values(by=["car_id"])

                df_feature_stats = pd.concat([df_feature_stats, _get_feature_stats(
                    make, model, df_features, feature_list)]).sort_values(by=["make", "model"])

        df_feature_stats['car'] = df_feature_stats[["make", "model"]].apply(
            lambda row: ' '.join(row.values.astype(str)), axis=1)
        df.drop(columns=['make', 'model'], inplace=True)
        df_feature_stats = df_feature_stats.sort_values(by=["feature"])

    return df_feature_stats


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


def get_video_ids_for_car_id(car_id):
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


def get_num_comments_for_video_id(video_id):
    supabase = init()
    num_comments = supabase.table("CONTENT").select(
        "content_id", count="exact").eq("video_id", video_id).execute().count
    return num_comments


def get_num_comments_for_make_and_model(make, model):
    """
    Get number of comments for make and model
    Multiple car_ids can exist per make and model (trim and year may differ)
    Multiple video_ids can exist per car_id
    """
    def _get_previews():
        """
        Return dict with previews for form preview values
        """
        return {"make": "Any make", "model": "Any model", "trim": "Any trim", "year": "Any year"}

    previews = _get_previews()

    if (make == previews["make"] and model == previews["model"]):
        return 0

    if (make != "" and make != previews["make"]):
        if (model != "" and model != previews["model"]):
            car_ids = get_car_id(make, model)
        else:
            car_ids = get_car_id(make, "")
    else:
        return ""

    num_comments = 0
    if isinstance(car_ids, int):
        car_id = car_ids
        num_comments += get_comment_count_actual_for_car_id(car_id)
    else:
        for car_id in car_ids:
            num_comments += get_comment_count_actual_for_car_id(car_id)
    return num_comments


def get_comment_count_actual_for_car_id(car_id):
    supabase = init()
    data = supabase.table("META").select(
        "comment_count_actual").eq("car_id", car_id).execute()
    sum = 0
    for i in data.data:
        sum += i["comment_count_actual"]
    return int(sum)


def get_comment_count_actual_for_video_id(video_id):
    supabase = init()
    data = supabase.table("META").select(
        "comment_count_actual").eq("video_id", video_id).execute()
    return int(data.data[0]["comment_count_actual"])


def get_car_from_car_id(car_id):
    supabase = init()
    data = supabase.table("CAR").select(
        "*").eq("car_id", car_id).execute()
    return data.data[0]


def get_make_from_car_id(car_id):
    supabase = init()
    data = supabase.table("CAR").select(
        "make").eq("car_id", car_id).execute()
    return data.data[0]["make"]


def get_model_from_car_id(car_id):
    supabase = init()
    data = supabase.table("CAR").select(
        "model").eq("car_id", car_id).execute()
    return data.data[0]["model"]


def get_models_of_make(make):
    supabase = init()
    data = supabase.table("CAR").select(
        "model").eq("make", make).execute()
    models = []
    for i in data.data:
        models.append(i["model"])
    return models


def video_id_exists(video_id):
    supabase = init()
    data = supabase.table("META").select(
        "video_id").eq("video_id", video_id).execute()
    if data.data:
        return True
    else:
        return False


def post_comment_count_actual(video_id, num_comments):
    supabase = init()
    supabase.table("META").update({
        "comment_count_actual": num_comments
    }).eq("video_id", video_id).execute()
    return "Insert executed: {} {}".format(video_id, num_comments)


def get_all_video_ids():
    supabase = init()
    data = supabase.table("META").select("video_id").execute()
    return data.data


def main():
    print(get_comment_count_actual_for_video_id("hCcbz8B64yk"))
    # for i in get_all_video_ids():
    #     video_id = i["video_id"]
    #     print(post_comment_count_actual(video_id, len(get_content(video_id))))


if __name__ == "__main__":
    main()
