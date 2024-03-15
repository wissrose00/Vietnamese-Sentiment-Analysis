import re
import requests
import pandas as pd
from youtube_comment_downloader import YoutubeCommentDownloader
import csv
from urllib.parse import urlparse

# cào bình luận shoppe
def scrape_shopee_comments(url, output_file):
    def extract_ids(url):
        match = re.search(r"i\.(\d+)\.(\d+)", url)
        return match.group(1), match.group(2)

    def fetch_comments(shop_id, item_id, offset):
        ratings_url = f"https://shopee.vn/api/v2/item/get_ratings?filter=0&flag=1&itemid={item_id}&limit=20&offset={offset}&shopid={shop_id}&type=0"
        data = requests.get(ratings_url).json()
        return data["data"]["ratings"] if "ratings" in data.get("data", {}) else []

    shop_id, item_id = extract_ids(url)
    offset = 0
    comments = []
    i = 1
    while True:
        ratings = fetch_comments(shop_id, item_id, offset)
        
        # Check if ratings is not None before iterating
        if ratings is not None:
            for index, rating in enumerate(ratings, i):
                comments.append(f"{index}. {rating['comment']}")
                print(f"{index}. {rating['comment']}")
            i += len(ratings)
        
        if not ratings or len(ratings) < 20:
            break

        offset += 20

    df = pd.DataFrame({"comment": comments})
    print(df)
    df.to_csv(output_file, index=False)

# lấy id của video 
def extract_video_id(youtube_url):
    query = urlparse(youtube_url)
    if query.hostname == 'www.youtube.com':
        if 'v' in query.query:
            return query.query.split('v=')[1]
    elif query.hostname == 'youtu.be':
        return query.path[1:]
    return None
# cào bình luận youtube
def scrape_youtube_comments(youtube_url, output_file):
    video_id = extract_video_id(youtube_url)
    
    if video_id is None:
        print("Invalid YouTube URL.")
        return
    
    downloader = YoutubeCommentDownloader()
    comments = downloader.get_comments(youtube_id=video_id)
    pattern = r"(\d+\..*)"
    
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["comment"])
        
        for comment in comments:
            text = f"{comment['text']}"
           

            match = re.search(pattern, text)
            if match:
                writer.writerow([match.group(1)])

# cào cmt từ 1 post trên facebook
def extract_post_id_from_url(url):
    parts = url.rstrip('/').split('/')
    if len(parts) >= 2:
        return parts[-1]
    else:
        raise ValueError("Invalid Facebook Group Post URL")
    

def scrape_facebook_comments(url , output_file):
    post_id = extract_post_id_from_url(url)
    access_token = 'xxxx'  
    comments = []
    url = f'https://graph.facebook.com/v17.0/{post_id}/comments?access_token={access_token}'

    while True:
        response = requests.get(url)
        data = response.json()
        if 'data' in data:
            comments.extend(data['data'])

            for comment in data['data']:
                if 'id' in comment:
                    replies_url = f'https://graph.facebook.com/v17.0/{comment["id"]}/comments?access_token={access_token}'
                    replies = requests.get(replies_url).json().get('data', [])
                    comments.extend(replies)

        if 'paging' in data and 'next' in data['paging']:
            url = data['paging']['next']
        else:
            break
   
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["comment"])

        for comment in comments:
            text = f" {comment.get('message', '')}"
            
            writer.writerow([text])
           
    return comments



# Sử dụng hàm với tham số là URL và tên file đầu ra
#scrape_shopee_comments("https://shopee.vn/G%C6%B0%C6%A1ng-Tu%E1%BA%A5n-T%C3%BA-Decor-To%C3%A0n-Th%C3%A2n-L%C6%B0%E1%BB%A3n-S%C3%B3ng-Khung-G%E1%BB%97-S%C6%A1n-2-%C4%90%E1%BA%A7u-Thon-Cao-C%E1%BA%A5p-i.1062313738.22853823189?xptdk=6aa6b085-65f3-4152-8d2e-026b902fa2c5", "./data/shoppe_comments.csv")
#scrape_youtube_comments("https://www.youtube.com/watch?v=-DKIgm-evsU", "./data/youtube_comments.csv")
#scrape_facebook_comments('https://www.facebook.com/groups/daihockiengiang/posts/1421205221822019/', 'facebook_comments.csv')
