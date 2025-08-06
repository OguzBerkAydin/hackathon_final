import { useState } from 'react';
import axios from 'axios';
import { Search, BrainCircuit } from 'lucide-react';

import SearchForm from './components/SearchForm';
import LoadingSpinner  from './components/LoadingSpinner';
import RecommendationDisplay  from './components/RecommendationDisplay';

import type { RecommendationResponse } from './types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8801';

function App() {
  const [userInput, setUserInput] = useState<string>('');
  const [recommendation, setRecommendation] = useState<RecommendationResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!userInput.trim()) {
      setError('Lütfen bir ürün veya kategori girin.');
      return;
    }

    setIsLoading(true);
    setError(null);
    setRecommendation(null);

    try {
      const response = await axios.post(
        `${API_BASE_URL}/recommend`,
        { user_input: userInput }
      );
      setRecommendation(response.data);
    } catch (err) {
      console.error(err);
      if (axios.isAxiosError(err) && err.response) {
        setError(`Bir hata oluştu: ${err.response.data.detail || err.message}`);
      } else {
        setError('Sunucuya bağlanılamadı. Backend uygulamasının çalıştığından emin olun.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 font-sans p-4 sm:p-6 lg:p-8">
      <main className="max-w-4xl mx-auto">
        {/* Header */}
        <header className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-2">
            <BrainCircuit className="h-10 w-10 text-cyan-400" />
            <h1 className="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 text-transparent bg-clip-text">
              Akıllı Ürün Ajanı
            </h1>
          </div>
          <p className="text-gray-400">Ne aradığınızı söyleyin, sizin için en iyisini bulalım.</p>
        </header>

        {/* Search Form */}
        <SearchForm
          userInput={userInput}
          setUserInput={setUserInput}
          handleSubmit={handleSubmit}
          isLoading={isLoading}
        />

        {/* Results Area */}
        <div className="mt-8">
          {isLoading && <LoadingSpinner />}
          {error && (
            <div className="bg-red-900/50 border border-red-700 text-red-300 px-4 py-3 rounded-md text-center">
              <p>{error}</p>
            </div>
          )}
          {recommendation ? (
            <RecommendationDisplay data={recommendation} />
          ) : (
            !isLoading && !error && (
              <div className="text-center text-gray-500 mt-16 flex flex-col items-center gap-4">
                <Search className="h-12 w-12" />
                <p>Örnek: "oyuncu bilgisayarı", "kaliteli bir kahve makinesi", "bebekler için en iyi araba koltuğu"</p>
              </div>
            )
          )}
        </div>
      </main>
      
      <footer className="text-center text-gray-600 mt-12 text-sm">
        <p>&copy; {new Date().getFullYear()} Akıllı Ürün Öneri Sistemi. React & FastAPI.</p>
      </footer>
    </div>
  );
}

export default App;