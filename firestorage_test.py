import toml
from firebase_admin import credentials, initialize_app, storage
# Init firebase with your credentials
cred = credentials.Certificate(toml.load(".streamlit/secrets.toml")["firebase_key"])
initialize_app(cred, {'storageBucket': 'analytics-44b35.appspot.com'})

# Put your local file path 
fileName = "myImage.jpg"
bucket = storage.bucket()
blob = bucket.blob(fileName)
blob.upload_from_file(fileName)

# Opt : if you want to make public access from the URL
blob.make_public()

print("your file url", blob.public_url)