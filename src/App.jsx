import { useState, useEffect } from 'react';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from './firebase';
import SearchBar from './components/SearchBar';
import VideoGrid from './components/VideoGrid';
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
    setCurrentIndex(newPlaylist.findIndex(v => v.id === video.id));
  };

  const nextVideo = () => {
    if (playlist.length === 0) return;
    const nextIndex = (currentIndex + 1) % playlist.length;
    setCurrentIndex(nextIndex);
    setCurrentVideo(playlist[nextIndex]);
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-white flex">
      {/* Sidebar Playlists */}
      <PlaylistSidebar 
        user={user} 
        playlist={playlist} 
        playVideo={playVideo}
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        <SearchBar onVideoSelect={playVideo} />

        <div className="flex-1 p-4">
          {currentVideo ? (
            <VideoPlayer 
              video={currentVideo} 
              onEnded={nextVideo} 
            />
          ) : (
            <div className="h-full flex items-center justify-center text-gray-500">
              Recherche une vidéo pour commencer
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
