from pyyoutube import Api
from pytube import YouTube
import os

api = Api(api_key="AIzaSyD58hj2H0hsJHo9myx--HvoZkFUCJSVBaQ")


def get_videos(channel_id):
    channel_info = api.get_channel_info(channel_id=channel_id)
    playlist_id = channel_info.items[0].contentDetails.relatedPlaylists.uploads
    uploads_playlist_items = api.get_playlist_items(
        playlist_id=playlist_id, count=100, limit=6
    )
    videos = []
    for item in uploads_playlist_items.items:
        video_id = item.contentDetails.videoId
        video = api.get_video_by_id(video_id=video_id)
        videos.extend(video.items)
    return videos


def processor(output_directory, channel_id):
    videos = get_videos(channel_id)
    for video in videos:
        url = f"https://www.youtube.com/watch?v={video.id}"
        print(f'Downloading "{video.snippet.title}"...')
        YouTube(url).streams.filter(res="360p").first().download(output_directory)


if __name__ == "__main__":
    processor(output_directory="videos", channel_id="UChIq04uLIDJfp1v647-5N_g")
