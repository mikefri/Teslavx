import requests
from bs4 import BeautifulSoup
import json
import random

def get_xvideos_gay():
    url = "https://www.xvideos.com/gay"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    results = []
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # XVideos utilise souvent l'ID 'video-id-...' pour ses div
        videos = soup.find_all('div', class_='thumb-block')
        
        for vid in videos:
            try:
                title = vid.find('p', class_='title').text.strip()
                link = "https://www.xvideos.com" + vid.find('p', class_='title').find('a')['href']
                img_tag = vid.find('div', class_='thumb').find('img')
                # On gère le "lazy loading" des images
                thumb = img_tag.get('data-src') or img_tag.get('src')
                
                results.append({"title": title, "link": link, "thumb": thumb, "source": "XVideos"})
            except:
                continue
    except Exception as e:
        print(f"Erreur XVideos: {e}")
    return results

def get_xhamster_gay():
    url = "https://xhamster.com/gay"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    results = []
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # XHamster utilise des classes 'video-thumb'
        videos = soup.find_all('div', class_='video-thumb')
        
        for vid in videos:
            try:
                # Recherche du lien et du titre
                link_tag = vid.find('a', class_='video-thumb__image-container')
                link = link_tag['href']
                title = vid.find('div', class_='video-thumb__info').find('a').text.strip()
                img_tag = vid.find('img')
                thumb = img_tag.get('src')
                
                results.append({"title": title, "link": link, "thumb": thumb, "source": "XHamster"})
            except:
                continue
    except Exception as e:
        print(f"Erreur XHamster: {e}")
    return results

def save_data():
    all_videos = get_xvideos_gay() + get_xhamster_gay()
    # On mélange pour avoir un mix des deux sites
    random.shuffle(all_videos)
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(all_videos, f, indent=4, ensure_ascii=False)
    print(f"Succès ! {len(all_videos)} vidéos récupérées.")

if __name__ == "__main__":
    save_data()
