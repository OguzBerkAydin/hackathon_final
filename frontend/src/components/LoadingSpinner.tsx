const LoadingSpinner = () => {
  return (
    <div className="flex flex-col items-center justify-center gap-4 py-12">
      <div className="w-12 h-12 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
      <p className="text-gray-400">Akıllı ajan sizin için araştırma yapıyor...</p>
    </div>
  );
};

export default LoadingSpinner;