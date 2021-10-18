import requests
import sys
import json
import re

def get_public_video_json(video_id : str):
    # Request
    # GET https://vk.com/al_video.php

    try:
        response = requests.get(
            url="https://vk.com/al_video.php",
            params={
                "act": "show",
                "al": "1",
                "autoplay": "1",
                "force_no_repeat": "1",
                "list": "null",
                "module": "profile_videos",
                "playlist_id": "546895073_-2",
                "preload": "1",
                "show_next": "1",
                "video": video_id,
            },
            headers={
                "X-Requested-With": "XMLHttpRequest",
                "Sec-Fetch-Dest": "empty",
                "authority": "vk.com",
                "sec-ch-ua": "Chromium;v=94, Google Chrome;v=94, ;Not A Brand;v=99",
                "sec-ch-ua-mobile": "?0",
                "Content-Type": "application/x-www-form-urlencoded",
                "Sec-Fetch-Site": "same-origin",
                "Origin": "https://vk.com",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
                "Sec-Fetch-Mode": "cors",
                "Cookie": "remixlang=3; remixstid=1106908445_Tp35ymRzlCzBxJX2pw3DdfyTI1iEWEawMFKYigwkjzD; remixlgck=da3008bf84f9ba5835; remixlhk=8c318dffb641991769; remixQUIC=1",
                "Referer": "https://vk.com/video{v_id}".format(v_id=video_id),
                "sec-ch-ua-platform": "macOS",
                "DNT": "1",
                "Accept-Language": "en-US,en;q=0.9,my;q=0.8",
                "Accept": "*/*",
            },
        )
                
        strResponse = response.content.decode("utf-8","ignore")

        # is this really public video?
        if re.search(r'<!>Please log in or <', strResponse):
            print("Need user to login.")
            return []

        # youtube video check
        isYouTubeVid = re.search(r'src="(https://www.youtube.com/.*?)"', strResponse)
        if isYouTubeVid is not None:
            print("We don't support youtube video here")
            return []

        if response.status_code != 200:
            print("Status Code : " + str(response.status_code))
            return []
        
        # starts parsing as json
        result = json.loads(strResponse.strip())
        return result

    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def getVideoIdFromUrl(url:str):

    # https://regexr.com/397dr

    # https://www.regextester.com/100027
    _VALID_URL = r'((\bvideo)(\-*)(\d+)_(\d+))|((\bvideos\b)(\-*)(\d+)_(\d+))|((\bvideo)(\d+)_(\d+))'

    id_list = re.findall(_VALID_URL, url)
    
    video_id = ""

    if len(id_list) > 0:
        video_id = id_list[0][0]

        if video_id.startswith("videos"):
            video_id = video_id.replace('videos', '')
        
        video_id = video_id.replace('video', '')

    return video_id

def printVideoUrlsFromResponse(jsonResponse:dict):

    resolutions = [ "240", "360", "480", "720", "1024" ]

    print("\nAvailable resolutions:")
    
    for i in resolutions:
        try:
            # https://github.com/KhunHtetzNaing/xGetter/blob/master/xgetter/src/main/java/com/htetznaing/lowcostvideo/Sites/VK.java
            
            s = jsonResponse["payload"][1][4]["player"]["params"][0]["url" + i]
            if s:
                print("\n" + i + "P : \n" + s )
        except Exception as e:
            continue

    return

def main():

    if len(sys.argv) < 2:
        print("")
        print("VK Video Info Extractor")
        print("")
        print("python3 main.py https://vk.com/video546895073_456247472")
        return
    
    link = sys.argv[1]

    video_id = getVideoIdFromUrl(link)

    response_json = get_public_video_json(video_id)

    printVideoUrlsFromResponse(response_json)

    return


if __name__ == "__main__":
    main()