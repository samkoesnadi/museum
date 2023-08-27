"""
To upload
"""
import glob
import multiprocessing
import os
from joblib import Parallel, delayed  

import tqdm
from bs4 import BeautifulSoup

from youtube_upload.client import YoutubeUploader

uploader = YoutubeUploader(secrets_file_path="client_secret_51351923137-4e24fhrvromp18rmf4iuvc3hcidk5eg1.apps.googleusercontent.com.json")
uploader.authenticate()

VIDEO_PATH = "f:\PRIVATE\M4ROOT\CLIP"

def upload(file_path):
    uploader.authenticate()

    print("Handling", file_path)

     # Extract date from xml
    with open(glob.glob(file_path[:-4] + "*.XML")[0], 'r') as f:
        xml = f.read()
    xml_data = BeautifulSoup(xml, "xml")
    title = xml_data.find("CreationDate").attrs["value"][:-6].replace("T", " ")

    # Video options
    options = {
        "title" : title, # The video title
        "description" : "", # The video description
        "tags" : ["vlog", "museum-of-sams-life"],
        "categoryId" : "22",
        "privacyStatus" : "private", # Video privacy. Can either be "public", "private", or "unlisted"
        "kids" : False, # Specifies if the Video if for kids or not. Defaults to False.
        # "thumbnailLink" : "https://cdn.havecamerawilltravel.com/photographer/files/2020/01/youtube-logo-new-1068x510.jpg" # Optional. Specifies video thumbnail.
    }

    # upload video
    uploader.upload(file_path, options) 


Parallel(n_jobs=4, verbose=10)(delayed(upload)(file_path) for file_path in tqdm.tqdm(glob.glob(os.path.join(VIDEO_PATH, "*.MP4"))))

uploader.close()
