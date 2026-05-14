import { useEffect, useRef } from 'react';

export default function VideoPlayer({ video, onEnded }) {
  const iframeRef = useRef(null);

  useEffect(() => {
    if (!video) return;

    // Écouteur pour savoir quand la vidéo se termine (un peu tricky avec iframe)
    const handleMessage = (event) => {
      if (event.origin !== "https://www.eporner.com") return;
      // Eporner envoie parfois des messages
      if (event.data?.event === "ended" || event.data?.time === "end") {
        onEnded();
      }
    };

    window.addEventListener("message", handleMessage);
    return () => window.removeEventListener("message", handleMessage);
  }, [video, onEnded]);

  if (!video) return null;

  return (
    <div className="aspect-video bg-black rounded-xl overflow-hidden">
      <iframe
        ref={iframeRef}
        src={`https://www.eporner.com/embed/${video.id}`}
        className="w-full h-full"
        allowFullScreen
        allow="autoplay; encrypted-media"
      />
      <div className="mt-3 px-2">
        <h2 className="text-xl font-bold">{video.title}</h2>
        <p className="text-gray-400 text-sm">{video.length} • {video.views} vues</p>
      </div>
    </div>
  );
}
