from pyyoutube import Api
from tqdm import tqdm
from pytube import YouTube
import os

api = Api(api_key="AIzaSyD58hj2H0hsJHo9myx--HvoZkFUCJSVBaQ")


def get_videos(channel_id):
    channel_info = api.get_channel_info(channel_id=channel_id)
    playlist_id = channel_info.items[0].contentDetails.relatedPlaylists.uploads
    uploads_playlist_items = api.get_playlist_items(
        playlist_id=playlist_id, count=1000, limit=6
    )
    videos = []
    for item in uploads_playlist_items.items:
        video_id = item.contentDetails.videoId
        video = api.get_video_by_id(video_id=video_id)
        videos.extend(video.items)
    return videos


def processor(output_directory, channel_id):
    videos = get_videos(channel_id)
    for video in tqdm(videos):
        url = f"https://www.youtube.com/watch?v={video.id}"
        if os.path.exists(os.path.join(output_directory, f"{video.snippet.title}.mp4")):
            print(f'Already downloaded "{video.snippet.title}')
            continue
        try:
            YouTube(url).streams.filter(res="360p").first().download(output_directory)
        except Exception as e:
            print(f"Error {e} - {video.snippet.title}")
            continue


if __name__ == "__main__":
    processor(output_directory="videos", channel_id="UChIq04uLIDJfp1v647-5N_g")
