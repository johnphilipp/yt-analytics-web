# export GOOGLE_APPLICATION_CREDENTIALS="/Users/philippjohn/Developer/youtube-analytics/keys/firebase_key.json"

import toml
import firebase_admin
from firebase_admin import credentials, firestore
import json

def firebase_init():
	cred = firebase_admin.credentials.Certificate(toml.load(".streamlit/secrets.toml")["firebase_key"])
	default_app = firebase_admin.initialize_app(cred, {
		"databaseURL": "https://analytics-44b35.firebaseio.com"
		})

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

def get_video_stats(db, brand, model, video_id):
	return db.collection("cars").document(brand).collection(model).document(video_id).get().to_dict()

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

	model = models[0]
	video_ids = get_video_ids(db, brand, model)
	print(video_ids) # ['abc123', 'pop789']
	print("")

	video_id = video_ids[0]
	thumbnail_url = get_thumbnail_url(db, video_id)
	print(thumbnail_url) # 
	print("")

	video_stats = get_video_stats(db, brand, model, video_id)
	print(video_stats)

	print(post_content(db, "Porsche", "911 GT3", "xxx"))

if __name__ == '__main__':
    main()

# query_ref = cars_ref.where(u'video_id', u'==', u'abc123').get()
# for post in query_ref:
#     print(u'{} => {}'.format(post.id, post.to_dict()))