import { useState } from 'react';
import { collection, addDoc } from 'firebase/firestore';
import { db, auth } from '../firebase';

export default function PlaylistModal({ isOpen, onClose, playlist, loadPlaylists }) {
  const [name, setName] = useState("Ma nouvelle playlist");

  const savePlaylist = async () => {
    if (!auth.currentUser || playlist.length === 0) return;

    try {
      await addDoc(collection(db, "playlists"), {
        userId: auth.currentUser.uid,
        name: name,
        videos: playlist,
        createdAt: new Date()
      });
      alert("✅ Playlist sauvegardée avec succès !");
      loadPlaylists();
      onClose();
    } catch (error) {
      console.error(error);
      alert("Erreur lors de la sauvegarde");
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50">
      <div className="bg-zinc-900 rounded-xl p-6 w-full max-w-md">
        <h2 className="text-2xl font-bold mb-4">Sauvegarder la playlist</h2>
        
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full bg-zinc-800 text-white px-4 py-3 rounded-lg mb-6 focus:outline-none focus:ring-2 focus:ring-red-500"
          placeholder="Nom de la playlist"
        />

        <div className="flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 py-3 bg-zinc-700 hover:bg-zinc-600 rounded-lg"
          >
            Annuler
          </button>
          <button
            onClick={savePlaylist}
            className="flex-1 py-3 bg-green-600 hover:bg-green-700 rounded-lg font-medium"
          >
            Sauvegarder
          </button>
        </div>
      </div>
    </div>
  );
}
