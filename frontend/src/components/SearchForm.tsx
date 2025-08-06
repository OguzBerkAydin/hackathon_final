import { Search } from 'lucide-react';

interface SearchFormProps {
  userInput: string;
  setUserInput: (value: string) => void;
  handleSubmit: (e: React.FormEvent) => void;
  isLoading: boolean;
}

const SearchForm: React.FC<SearchFormProps> = ({ userInput, setUserInput, handleSubmit, isLoading }) => {
  return (
    <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-2">
      <input
        type="text"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        placeholder="Örn: Uygun fiyatlı bir 4K televizyon..."
        className="flex-grow bg-gray-800 border border-gray-700 rounded-md px-4 py-3 focus:ring-2 focus:ring-cyan-500 focus:outline-none transition"
        disabled={isLoading}
      />
      <button
        type="submit"
        className="flex items-center justify-center gap-2 bg-cyan-600 hover:bg-cyan-700 text-white font-bold py-3 px-6 rounded-md transition duration-200 disabled:bg-gray-600 disabled:cursor-not-allowed"
        disabled={isLoading}
      >
        <Search className="h-5 w-5" />
        <span>Öneri Getir</span>
      </button>
    </form>
  );
};

export default SearchForm;
