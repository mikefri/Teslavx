import requests
from bs4 import BeautifulSoup
import json
import random
import re

def extract_id(url):
    # Cherche l'ID dans le format video.xxxx ou video12345
    match = re.search(r'video\.?([^/?]+)', url)
    if match:
        video_id = match.group(1)
        # Nettoyage si l'ID a récupéré des paramètres inutiles
        if "." in video_id and len(video_id) < 5: # Cas du s.com
            return None
        return video_id
    return None

def get_xvideos_gay():
    url = "https://www.xvideos.com/gay"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    results = []
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        videos = soup.find_all('div', class_='thumb-block')
        
        for vid in videos:
            try:
                raw_link = "https://www.xvideos.com" + vid.find('p', class_='title').find('a')['href']
                video_id = extract_id(raw_link)
                
                if video_id:
                    title = vid.find('p', class_='title').text.strip()
                    img_tag = vid.find('div', class_='thumb').find('img')
                    thumb = img_tag.get('data-src') or img_tag.get('src')
                    
                    results.append({
                        "title": title, 
                        "link": raw_link, 
                        "embed_url": f"https://www.xvideos.com/embedframe/{video_id}",
                        "thumb": thumb, 
                        "source": "XVideos"
                    })
            except: continue
    except Exception as e: print(f"Erreur XVideos: {e}")
    return results

# ... (Garder la fonction xhamster sur le même modèle si besoin) ...

def save_data():
    all_videos = get_xvideos_gay()
    random.shuffle(all_videos)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(all_videos, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    save_data()
