import requests
from bs4 import BeautifulSoup
import json
import os
import random
import re
import time

# --- EXTRATEURS D'IDS ---

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

def extract_xhamster_id(url_string):
    # XHamster stocke ses IDs sous la forme xh12345 ou dans l'URL directement
    match = re.search(r'(xh[a-zA-Z0-9]+)', url_string)
    if match:
        return match.group(1)
    return None

# --- SCRAPER XVIDEOS ---

def get_xvideos_page(page_number):
    url = f"https://www.xvideos.com/gay/new/{page_number}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    results = []
    
    try:
        print(f"[XVideos] Scraping de la page {page_number}...")
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
                        "title": f"[XV] {title}", 
                        "link": "https://www.xvideos.com" + href, 
                        "embed_url": f"https://www.xvideos.com/embedframe/{video_id}",
                        "thumb": thumb, 
                        "source": "XVideos"
                    })
            except: continue
    except Exception as e:
        print(f"Erreur XVideos page {page_number}: {e}")
    return results

# --- SCRAPER XHAMSTER ---

def get_xhamster_page(page_number):
    # Section Gay / Nouveautés sur XHamster
    url = f"https://fr.xhamster.com/gay/{page_number}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    results = []
    
    try:
        print(f"[XHamster] Scraping de la page {page_number}...")
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Sur XHamster, les vidéos sont généralement dans des balises avec data-role="video-thumb" ou class="video-thumb"
        videos = soup.find_all('div', class_='video-thumb')
        
        for vid in videos:
            try:
                a_tag = vid.find('a', class_='video-thumb__image-container')
                if not a_tag:
                    continue
                
                href = a_tag['href']
                video_id = extract_xhamster_id(href)
                
                if video_id:
                    title_tag = vid.find('a', class_='video-thumb__title')
                    title = title_tag.text.strip() if title_tag else "Vidéo XHamster Gay"
                    
                    img_tag = vid.find('img', class_='video-thumb__image')
                    thumb = img_tag.get('data-src') or img_tag.get('src') if img_tag else ""
                    
                    results.append({
                        "title": f"[XH] {title}",
                        "link": href,
                        "embed_url": f"https://xhamster.com/embed/{video_id}",
                        "thumb": thumb,
                        "source": "XHamster"
                    })
            except: continue
    except Exception as e:
        print(f"Erreur XHamster page {page_number}: {e}")
    return results

# --- FUSION ET SAUVEGARDE ---

def save_data():
    file_path = 'data.json'
    
    # 1. Charger l'historique pour ne rien perdre
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except:
                existing_data = []
    else:
        existing_data = []

    new_videos = []
    
    # 2. On récolte 5 pages sur XVideos
    for p in range(0, 5): 
        new_videos.extend(get_xvideos_page(p))
        time.sleep(1)

    # 3. On récolte 5 pages sur XHamster
    for p in range(1, 6): # XHamster commence souvent à la page 1
        new_videos.extend(get_xhamster_page(p))
        time.sleep(1)

    # 4. Fusion sans doublons (basée sur l'embed_url)
    combined_data = existing_data + new_videos
    unique_data = {v['embed_url']: v for v in combined_data}.values()
    final_list = list(unique_data)

    # 5. Mélange total pour avoir un flux dynamique
    random.shuffle(final_list)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=4, ensure_ascii=False)
    
    print(f"\nMise à jour terminée !")
    print(f"Total dans ta base privée : {len(final_list)} vidéos.")
    print(f"Ajouts lors de ce scan : {len(new_videos)} vidéos récoltées.")

if __name__ == "__main__":
    save_data()
