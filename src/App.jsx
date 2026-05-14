import { useState, useEffect } from 'react';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from './firebase';
import SearchBar from './components/SearchBar';
import VideoPlayer from './components/VideoPlayer';
import PlaylistSidebar from './components/PlaylistSidebar';

function App() {
  const [user, setUser] = useState(null);
  const [currentVideo, setCurrentVideo] = useState(null);
  const [playlist, setPlaylist] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    onAuthStateChanged(auth, (currentUser) => setUser(currentUser));
  }, []);

  const playVideo = (video, newPlaylist = playlist) => {
    setCurrentVideo(video);
    setPlaylist(newPlaylist);
    setCurrentIndex(newPlaylist.findIndex(v => v.id === video.id) || 0);
  };

  const nextVideo = () => {
    if (playlist.length <= 1) return;
    const nextIndex = (currentIndex + 1) % playlist.length;
    setCurrentIndex(nextIndex);
    setCurrentVideo(playlist[nextIndex]);
  };

  // Ajouter une vidéo à la playlist actuelle
  const addToPlaylist = (video) => {
    if (playlist.some(v => v.id === video.id)) {
      alert("Cette vidéo est déjà dans la playlist");
      return;
    }
    const newPlaylist = [...playlist, video];
    setPlaylist(newPlaylist);
  };

  // Supprimer une vidéo de la playlist
  const removeFromPlaylist = (videoId) => {
    const newPlaylist = playlist.filter(v => v.id !== videoId);
    setPlaylist(newPlaylist);

    // Si on supprime la vidéo en cours de lecture
    if (currentVideo && currentVideo.id === videoId) {
      if (newPlaylist.length > 0) {
        setCurrentVideo(newPlaylist[0]);
        setCurrentIndex(0);
      } else {
        setCurrentVideo(null);
      }
    }
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-white flex">
      <PlaylistSidebar 
        user={user}
        playlist={playlist}
        playVideo={playVideo}
        removeFromPlaylist={removeFromPlaylist}
        savePlaylist={() => {/* géré dans sidebar */}}
      />

      <div className="flex-1 flex flex-col">
        <SearchBar 
          onVideoSelect={playVideo} 
          addToPlaylist={addToPlaylist} 
        />

        <div className="flex-1 p-4">
          {currentVideo ? (
            <VideoPlayer 
              video={currentVideo} 
              onEnded={nextVideo} 
            />
          ) : (
            <div className="h-[70vh] flex items-center justify-center text-gray-500 text-xl">
              🔍 Recherche une vidéo pour commencer
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
