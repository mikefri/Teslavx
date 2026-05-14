import { useState } from 'react';

export default function SearchBar({ onVideoSelect }) {
  const [query, setQuery] = useState('');
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(false);

  const search = async () => {
    if (!query) return;
    setLoading(true);

    try {
      const res = await fetch(
        `https://www.eporner.com/api/v2/video/search/?query=${encodeURIComponent(query)}&per_page=24&thumbsize=big&order=latest&format=json`
      );
      const data = await res.json();
      setVideos(data.videos || []);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="p-4 border-b border-zinc-800">
      <div className="flex gap-3">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && search()}
          placeholder="Rechercher des vidéos..."
          className="flex-1 bg-zinc-900 text-white px-4 py-3 rounded-lg focus:outline-none"
        />
        <button
          onClick={search}
          disabled={loading}
          className="bg-red-600 hover:bg-red-700 px-8 rounded-lg font-medium"
        >
          {loading ? 'Recherche...' : 'Chercher'}
        </button>
      </div>

      <VideoGrid videos={videos} onVideoSelect={onVideoSelect} />
    </div>
  );
}
