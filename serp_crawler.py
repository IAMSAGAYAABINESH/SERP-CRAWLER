from serpapi import GoogleSearch
import pandas as pd
from googleapiclient.discovery import build
import streamlit as st

params={
    'api_key': 'd390e0da85bb6349030f1ae7197985e09363fbc87e44694dcd93c2b3f843f46a',
    'engine': 'google',
    'hl': 'en',
    'gl': 'in',
    'num': 10000,
    'q': "site:youtube.com openinapp.co"
}

youtube=build("youtube","v3",developerKey="AIzaSyDHZgTv-yOaP05p63ou7zxxe91Rbs7n6A0")

search=GoogleSearch(params)
results=search.get_dict()
organic_results=results["organic_results"]

channel_data=[]
for result in organic_results:
    title=result["title"]
    if "https://www.youtube.com/c/" in result["link"]:
        channel_id=result["link"].split("/")[4]
        channel_link="https://www.youtube.com/c/"+channel_id
        channel_data.append({"title":title,"link":channel_link})
    else:
        if "https://www.youtube.com/watch?" in result["link"]:
            video_id=result["link"].split("=")[1]
            video_response=youtube.videos().list(part="snippet",
                                                 id=video_id).execute()
            vid_channel_id=video_response["items"][0]["snippet"]["channelId"]
            vid_channel_link="https://www.youtube.com/channel/"+vid_channel_id
            channel_data.append({"title":title,"link":vid_channel_link})

df=pd.DataFrame.from_dict(channel_data)
st.title("SERP Crawler")
st.dataframe(df)
st.download_button(label="Download CSV",data=df.to_csv(),file_name="webcrawler.csv")            
