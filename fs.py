import toml
import firebase_admin
from firebase_admin import db, storage

cred = firebase_admin.credentials.Certificate(toml.load(".streamlit/secrets.toml")["firebase_key"])
config = {"storageBucket": "analytics-44b35.appspot.com"}
app    = firebase_admin.initialize_app(cred, config)
bucket = storage.bucket(app=app)

def upload_df(df, video_id, file_name):
    """
    Upload a Dataframe as a csv to Firebase Storage
    :return: storage_ref
    """
    storage_ref = video_id + "/" + file_name + ".csv"
    blob = bucket.blob(storage_ref)
    blob.upload_from_string(df.to_csv())

    return storage_ref
    