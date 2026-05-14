import requests
from bs4 import BeautifulSoup
import json
import random

def extract_xvideos_id(url_path):
    """
    Découpe proprement l'URL pour en extraire l'identifiant unique.
    Exemple d'entrée : '/video.okfvaldfd69/home...' ou '/video654321/titre'
    """
    if not url_path or 'video' not in url_path:
        return None
        
    # On isole la partie qui contient le mot 'video'
    parts = url_path.split('/')
    video_part = next((p for p in parts if 'video' in p), None)
    
    if video_part:
        # On supprime le préfixe 'video.' ou 'video'
        video_id = video_part.replace('video.', '').replace('video', '')
        # Si le nettoyage renvoie un texte vide ou un bug comme 's.com'
        if not video_id or video_id == "s.com":
            return None
        return video_id
    return None

def get_xvideos_gay():
    url = "https://www.xvideos.com/gay"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    results = []
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Sélection des blocs de vidéos sur XVideos
        videos = soup.find_all('div', class_='thumb-block')
        
        for vid in videos:
            try:
                # Étape 1 : Trouver la balise du lien
                a_tag = vid.find('p', class_='title').find('a')
                href = a_tag['href'] # Contient souvent quelque chose comme /video.xxxx/titre
                
                # Étape 2 : Extraction chirurgicale de l'identifiant
                video_id = extract_xvideos_id(href)
                
                # Étape 3 : Si l'identifiant est introuvable avec la méthode 1, on tente la méthode 2 (via l'ID du bloc HTML)
                if not video_id and vid.has_attr('id'):
                    # Les blocs ont souvent un ID de type 'video_123456'
                    video_id = vid['id'].replace('video_', '')

                # Si on a un identifiant valide (et pas un s.com erroné)
                if video_id and video_id != "s.com":
                    title = a_tag.text.strip()
                    img_tag = vid.find('div', class_='thumb').find('img')
                    thumb = img_tag.get('data-src') or img_tag.get('src')
                    
                    # On construit l'URL de l'embed parfaite
                    embed_url = f"https://www.xvideos.com/embedframe/{video_id}"
                    raw_link = "https://www.xvideos.com" + href
                    
                    results.append({
                        "title": title, 
                        "link": raw_link, 
                        "embed_url": embed_url,
                        "thumb": thumb, 
                        "source": "XVideos"
                    })
            except Exception as e:
                continue # Ignore les erreurs mineures sur une seule miniature
                
    except Exception as e:
        print(f"Erreur globale lors du scraping XVideos: {e}")
        
    return results

def save_data():
    print("Lancement du scraper...")
    all_videos = get_xvideos_gay()
    
    # On mélange les résultats
    random.shuffle(all_videos)
    
    # Sauvegarde finale
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(all_videos, f, indent=4, ensure_ascii=False)
        
    print(f"Extraction terminée avec succès ! {len(all_videos)} vidéos trouvées.")

if __name__ == "__main__":
    save_data()
