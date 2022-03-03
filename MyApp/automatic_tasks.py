
from background_task import background
import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
from PIL import Image
import requests
from io import BytesIO
import time
import datetime
from django.http.response import HttpResponseRedirect
from django.utils import timezone
from Blog.Post.forms import ManagePostCreateForm
from django.core.files.base import ContentFile

@background(schedule=10)
def savePosts(s,t):
    try:
        url = s.get('playlist')
        query = parse_qs(urlparse(url).query, keep_blank_values=True)
        playlist_id = query["list"][0]
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = "AIzaSyBgzluEvlveyfNKaigwEClXvhSaUyTmLLI")
        api_request = youtube.playlistItems().list(part = "snippet",playlistId = playlist_id,maxResults = 50)
        response = api_request.execute()
        playlist_items = []
        while api_request is not None:
            response = api_request.execute()
            playlist_items.append(response["items"])
            api_request = youtube.playlistItems().list_next(api_request, response)
        video_data = []
        for i in playlist_items:
            for v in i:
                title = v.get('snippet').get("title")
                description = v.get('snippet').get("description")
                image = v.get('snippet').get('thumbnails').get('medium').get('url')
                img_responce = requests.get(image)
                img = Image.open(BytesIO(img_responce.content))
                img.convert('RGB')
                img.resize((img.size[0],img.size[1]),Image.ANTIALIAS)
                img_io = BytesIO()
                img.save(img_io, format='JPEG', quality=100)
                img_content = ContentFile(img_io.getvalue(),"img.jpg" )
                url = (f'https://www.youtube.com/watch?v={v["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s')
                video_data.append({"text" : title ,"description" : description ,"image" : img_content ,"url" : url})
        for i in video_data:
            form = ManagePostCreateForm({
                'name' : str("{} #{}".format(s.get("name"),str(video_data.index(i)+1))) ,
                'description' : i.get("text") ,
                'text' : i.get("description") ,
                'video' : i.get("url") ,
                'blog' : t ,
            },{
                'image' : i.get("image") ,
            })
            form.save()
    except:
        pass

