import requests
from bs4 import BeautifulSoup
import json
import os
import random
import time

def extract_xvideos_id(url_path):
    if not url_path or 'video' not in url_path:
        return None
    parts = url_path.split('/')
    video_part = next((p for p in parts if 'video' in p), None)
    if video_part:
        video_id = video_part.replace('video.', '').replace('video', '')
        if not video_id or video_id == "s.com":
            return None
        return video_id
    return None

def get_videos_from_page(page_number):
    # On cible spécifiquement la section gay avec pagination
    url = f"https://www.xvideos.com/gay/new/{page_number}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    results = []
    
    try:
        print(f"Scraping de la page {page_number}...")
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        videos = soup.find_all('div', class_='thumb-block')
        
        for vid in videos:
            try:
                a_tag = vid.find('p', class_='title').find('a')
                href = a_tag['href']
                video_id = extract_xvideos_id(href)
                
                if not video_id and vid.has_attr('id'):
                    video_id = vid['id'].replace('video_', '')

                if video_id and video_id != "s.com":
                    title = a_tag.text.strip()
                    img_tag = vid.find('div', class_='thumb').find('img')
                    thumb = img_tag.get('data-src') or img_tag.get('src')
                    
                    results.append({
                        "title": title, 
                        "link": "https://www.xvideos.com" + href, 
                        "embed_url": f"https://www.xvideos.com/embedframe/{video_id}",
                        "thumb": thumb, 
                        "source": "XVideos"
                    })
            except: continue
    except Exception as e:
        print(f"Erreur page {page_number}: {e}")
    return results

def save_data():
    file_path = 'data.json'
    
    # 1. Charger l'existant si le fichier existe
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except:
                existing_data = []
    else:
        existing_data = []

    # 2. Récupérer les nouvelles vidéos sur les 5 premières pages (tu peux monter à 10 ou 20)
    new_videos = []
    for p in range(0, 5): 
        new_videos.extend(get_videos_from_page(p))
        time.sleep(1) # Petite pause pour ne pas être banni

    # 3. Fusionner et supprimer les doublons basés sur l'embed_url
    combined_data = existing_data + new_videos
    # On utilise un dictionnaire pour garder l'unicité des IDs
    unique_data = {v['embed_url']: v for v in combined_data}.values()
    final_list = list(unique_data)

    # 4. Mélanger pour la variété et sauvegarder
    random.shuffle(final_list)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=4, ensure_ascii=False)
    
    print(f"Terminé ! Total dans la base : {len(final_list)} vidéos (dont {len(new_videos)} nouvelles).")

if __name__ == "__main__":
    save_data()
