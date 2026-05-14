import { useState, useEffect } from 'react';
import { collection, addDoc, getDocs, query, where, orderBy } from 'firebase/firestore';
import { db, auth } from '../firebase';
import { signInAnonymously } from 'firebase/auth';

export default function PlaylistSidebar({ playlist, playVideo }) {
  const [playlists, setPlaylists] = useState([]);
  const [currentPlaylistName, setCurrentPlaylistName] = useState("Ma Playlist");
  const [showModal, setShowModal] = useState(false);
  const [newPlaylistName, setNewPlaylistName] = useState("");

  // Connexion anonyme
  useEffect(() => {
    if (!auth.currentUser) {
      signInAnonymously(auth);
    }
  }, []);

  // Charger les playlists de l'utilisateur
  const loadPlaylists = async () => {
    if (!auth.currentUser) return;
    
    const q = query(
      collection(db, "playlists"),
      where("userId", "==", auth.currentUser.uid),
      orderBy("createdAt", "desc")
    );
    
    const snapshot = await getDocs(q);
    const userPlaylists = snapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
    setPlaylists(userPlaylists);
  };

  useEffect(() => {
    loadPlaylists();
  }, [auth.currentUser]);

  const saveCurrentPlaylist = async () => {
    if (!auth.currentUser || playlist.length === 0) return;

    try {
      await addDoc(collection(db, "playlists"), {
        userId: auth.currentUser.uid,
        name: currentPlaylistName,
        videos: playlist,
        createdAt: new Date()
      });
      alert("Playlist sauvegardée !");
      loadPlaylists();
    } catch (error) {
      console.error(error);
    }
  };

  const loadPlaylist = (pl) => {
    playVideo(pl.videos[0], pl.videos);
    setCurrentPlaylistName(pl.name);
  };

  return (
    <div className="w-80 bg-zinc-900 border-r border-zinc-800 flex flex-col">
      <div className="p-4 border-b border-zinc-800">
        <h1 className="text-2xl font-bold text-red-500">Eporner Playlist</h1>
      </div>

      <div className="p-4">
        <button
          onClick={saveCurrentPlaylist}
          className="w-full bg-green-600 hover:bg-green-700 py-3 rounded-lg font-medium mb-4"
        >
          💾 Sauvegarder cette playlist
        </button>

        <button
          onClick={() => setShowModal(true)}
          className="w-full bg-zinc-700 hover:bg-zinc-600 py-3 rounded-lg font-medium"
        >
          + Nouvelle Playlist
        </button>
      </div>

      <div className="px-4 text-sm text-gray-400 mb-2">Mes Playlists</div>
      <div className="flex-1 overflow-auto">
        {playlists.map(pl => (
          <div
            key={pl.id}
            onClick={() => loadPlaylist(pl)}
            className="px-4 py-3 hover:bg-zinc-800 cursor-pointer border-b border-zinc-800"
          >
            <div className="font-medium">{pl.name}</div>
            <div className="text-xs text-gray-500">{pl.videos.length} vidéos</div>
          </div>
        ))}
      </div>
    </div>
  );
}
