import urllib.parse
from pymongo import MongoClient

import streamlit as st
from pymongo import MongoClient

def get_collection():
    uri = st.secrets["MONGO_URI"]
    client = MongoClient(uri)
    db = client["movie_database"]
    return db["movies"]