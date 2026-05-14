export default function VideoGrid({ videos, onVideoSelect }) {
  const addToCurrentPlaylist = (video) => {
    // Cette fonction sera gérée dans le parent plus tard
    alert("Vidéo ajoutée à la playlist ! (à implémenter avec Firebase)");
  };

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 mt-6">
      {videos.map((video) => (
        <div
          key={video.id}
          className="bg-zinc-900 rounded-lg overflow-hidden hover:scale-105 transition-transform cursor-pointer group"
        >
          <div className="relative">
            <img
              src={video.thumb || video.default_thumb}
              alt={video.title}
              className="w-full aspect-video object-cover"
            />
            <div className="absolute bottom-1 right-1 bg-black/70 text-xs px-1.5 py-0.5 rounded">
              {video.length}
            </div>
          </div>

          <div className="p-3">
            <h3 className="font-medium text-sm line-clamp-2 h-10 group-hover:text-red-500 transition-colors">
              {video.title}
            </h3>
            <p className="text-gray-500 text-xs mt-2">
              {video.views} vues • {video.rating}%
            </p>

            <div className="flex gap-2 mt-3">
              <button
                onClick={() => onVideoSelect(video)}
                className="flex-1 bg-red-600 hover:bg-red-700 py-2 text-sm rounded font-medium"
              >
                Lire
              </button>
              <button
                onClick={() => addToCurrentPlaylist(video)}
                className="flex-1 bg-zinc-700 hover:bg-zinc-600 py-2 text-sm rounded font-medium"
              >
                + Playlist
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
