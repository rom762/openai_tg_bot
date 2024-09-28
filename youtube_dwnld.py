import yt_dlp as youtube_dl
import os


def is_exist(fname):
    return os.path.isfile(fname)


def download_mp3(url):
    video_info = youtube_dl.YoutubeDL().extract_info(url=url, download=False)
    filename = f"{video_info['title']}.mp3"
    print(filename)
    if not is_exist(filename):    
        options = {
              'format': 'bestaudio/best',
              'keepvideo': False,
              'outtmpl': filename,
        }

    try:
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])
    except Exception as e:
        result = f"ERROR, can't download this url"

    return filename


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=6pqOZq9eBBg"
    download_mp3(url)
