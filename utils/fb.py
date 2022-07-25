# export GOOGLE_APPLICATION_CREDENTIALS="/Users/philippjohn/Developer/youtube-analytics/keys/firebase_key.json"

import toml
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app, storage
import json
import pandas as pd

def firebase_init():
	cred = firebase_admin.credentials.Certificate(toml.load(".streamlit/secrets.toml")["firebase_key"])
	default_app = firebase_admin.initialize_app(cred, {
		"databaseURL": "https://analytics-44b35.firebaseio.com",
		'storageBucket': 'analytics-44b35.appspot.com'
		})







def upload_df(df, video_id, file_name):
	"""
	Upload a Dataframe as a csv to Firebase Storage
	:return: storage_ref
	"""
	bucket = storage.bucket()
	storage_ref = video_id + "/" + file_name + ".json"
	blob = bucket.blob(storage_ref)
	blob.upload_from_string(df.to_json())

	# # Opt : if you want to make public access from the URL
	# blob.make_public()

	return storage_ref


def download_df(video_id, file_name):
	"""
	Download a csv to Firebase Storage and convert to pandas df
	:return: storage_ref
	"""
	bucket = storage.bucket()
	storage_ref = video_id + "/" + file_name + ".json"
	blob = bucket.blob(storage_ref)
	data = blob.download_as_string().decode("utf-8")
	dict = json.loads(data)
	return pd.DataFrame.from_dict(dict)




def get_brands(db):
	brands = []
	for b in db.collection("cars").get():
		brands.append(b.id)
	return brands

def get_models(db, brand):
	models = []
	for m in db.collection('cars').document(brand).collections():
		models.append(m.id)
	return models

def get_video_ids(db, brand, model):
	video_ids = []
	for k in db.collection("cars").document(brand).collection(model).get():
		video_ids.append(k.id)
	return video_ids

#
#
#
# v v v TODO: This needs to be changed v v v
#
#
#
def get_data(db, brand, model, video_id, field="all"):
	if field == "all":
		return db.collection("cars").document(brand).collection(model).document(video_id).get().to_dict()
	else:
		return db.collection("cars").document(brand).collection(model).document(video_id).get().to_dict()[field]

def post_meta(db, brand, model, video_id, meta):
	keys = list(meta.keys())
	db.collection("cars").document(brand).collection(model).document(video_id).set({
		"meta": {
        keys[0]: meta["title"],
        keys[1]: meta["channel_title"],
        keys[2]: meta["thumbnail_url"],
        keys[3]: meta["published_at"],
        keys[4]: meta["view_count"],
        keys[5]: meta["like_count"],
        keys[6]: meta["comment_count"]
    }})
	return "Posted meta"

def post_content(db, brand, model, video_id, content_json):
	key = list(content_json.keys())[0]
	db.collection("cars").document(brand).collection(model).document(video_id).update({
		key: {
        key: json.dumps(content_json[key])
    }})
	return "Posted content"






def main():
	firebase_init()
	db = firestore.client()

	brands = get_brands(db)
	print(brands) # ['Porsche', 'Tesla']
	print("")

	brand = brands[0]
	models = get_models(db, brand)
	print(models) # ['911 GT3', '911 Sport Classic']
	print("")

	model = models[2]
	video_ids = get_video_ids(db, brand, model)
	print(video_ids) # ['abc123', 'pop789']
	print("")

	video_id = video_ids[0]
	# video_data = get_data(db, brand, model, video_id)
	# print(video_data, "\n")
	print(get_data(db, brand, model, video_id, field="meta"), "\n")
	print(get_data(db, brand, model, video_id, field="content_raw")["content_raw"], "\n")
	print(get_data(db, brand, model, video_id, field="sentiment_1")["sentiment_1"], "\n")
	print(get_data(db, brand, model, video_id, field="feature_stats")["feature_stats"], "\n")

	# print(post_content(db, "Porsche", "911 GT3", "xxx"))

if __name__ == '__main__':
    main()

# query_ref = cars_ref.where(u'video_id', u'==', u'abc123').get()
# for post in query_ref:
#     print(u'{} => {}'.format(post.id, post.to_dict()))