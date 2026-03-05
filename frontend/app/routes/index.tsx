import { createFileRoute } from '@tanstack/react-router'
import { useState } from 'react'
import { SearchBar } from '../components/SearchBar'
import { ResultCard } from '../components/ResultCard'
import { FilterPanel } from '../components/FilterPanel'
import { searchTorrents, type TorrentResult } from '../lib/api'
import { Magnet, Loader2 } from 'lucide-react'

export const Route = createFileRoute('/')({ 
  component: HomePage,
})

const CATEGORIES = ['all', 'movies', 'tv', 'anime', 'music', 'games', 'software']
const SOURCES_LIST = ['yts', 'nyaa', 'eztv', '1337x', 'tpb', 'rarbg', 'tgx', 'kat', 'lime']

export default function HomePage() {
  const [results, setResults] = useState<TorrentResult[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [query, setQuery] = useState('')
  const [category, setCategory] = useState('all')
  const [enabledSources, setEnabledSources] = useState<string[]>(SOURCES_LIST)
  const [searched, setSearched] = useState(false)

  const handleSearch = async (q: string) => {
    if (!q.trim()) return
    setQuery(q)
    setLoading(true)
    setError(null)
    setSearched(true)
    try {
      const data = await searchTorrents(q, category, enabledSources)
      setResults(data.results)
    } catch {
      setError('Erro ao buscar. Tente novamente.')
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="text-center mb-10">
        <div className="flex items-center justify-center gap-3 mb-3">
          <Magnet className="w-10 h-10 text-sky-400" />
          <h1 className="text-4xl font-bold text-white">Torrent Search</h1>
        </div>
        <p className="text-gray-400">Busca unificada em {SOURCES_LIST.length} fontes &bull; magnet links diretos</p>
      </div>

      <SearchBar onSearch={handleSearch} loading={loading} />

      <FilterPanel
        categories={CATEGORIES}
        selectedCategory={category}
        onCategoryChange={setCategory}
        sources={SOURCES_LIST}
        enabledSources={enabledSources}
        onSourceToggle={(s) =>
          setEnabledSources(prev =>
            prev.includes(s) ? prev.filter(x => x !== s) : [...prev, s]
          )
        }
      />

      <div className="mt-6">
        {loading && (
          <div className="flex justify-center py-16">
            <Loader2 className="w-8 h-8 animate-spin text-sky-400" />
          </div>
        )}
        {error && <div className="text-center py-12 text-red-400">{error}</div>}
        {!loading && searched && results.length === 0 && !error && (
          <div className="text-center py-12 text-gray-500">Nenhum resultado para "{query}"</div>
        )}
        {!loading && results.length > 0 && (
          <>
            <p className="text-sm text-gray-500 mb-4">{results.length} resultados para "{query}"</p>
            <div className="space-y-3">
              {results.map((r, i) => <ResultCard key={i} result={r} />)}
            </div>
          </>
        )}
      </div>
    </div>
  )
}
