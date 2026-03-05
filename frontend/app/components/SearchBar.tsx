import { useState, type KeyboardEvent } from 'react'
import { Search } from 'lucide-react'

interface Props {
  onSearch: (q: string) => void
  loading: boolean
}

export function SearchBar({ onSearch, loading }: Props) {
  const [value, setValue] = useState('')
  const handleKey = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') onSearch(value)
  }
  return (
    <div className="flex gap-2 max-w-2xl mx-auto">
      <input
        type="text"
        value={value}
        onChange={e => setValue(e.target.value)}
        onKeyDown={handleKey}
        placeholder="Buscar filmes, séries, anime, jogos..."
        className="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500"
      />
      <button
        onClick={() => onSearch(value)}
        disabled={loading || !value.trim()}
        className="bg-sky-600 hover:bg-sky-500 disabled:opacity-50 disabled:cursor-not-allowed px-6 py-3 rounded-lg font-medium transition-colors flex items-center gap-2"
      >
        <Search className="w-4 h-4" />
        Buscar
      </button>
    </div>
  )
}
