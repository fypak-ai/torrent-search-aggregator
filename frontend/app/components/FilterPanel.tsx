interface Props {
  categories: string[]
  selectedCategory: string
  onCategoryChange: (c: string) => void
  sources: string[]
  enabledSources: string[]
  onSourceToggle: (s: string) => void
}

const SOURCE_LABELS: Record<string, string> = {
  yts: 'YTS', nyaa: 'Nyaa', eztv: 'EZTV', '1337x': '1337x', tpb: 'TPB', rarbg: 'RARBG',
}

export function FilterPanel({ categories, selectedCategory, onCategoryChange, sources, enabledSources, onSourceToggle }: Props) {
  return (
    <div className="mt-6 space-y-4 max-w-4xl mx-auto">
      <div className="flex flex-wrap gap-2">
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => onCategoryChange(cat)}
            className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors capitalize ${
              selectedCategory === cat
                ? 'bg-sky-600 text-white'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>
      <div className="flex flex-wrap gap-2">
        {sources.map(src => (
          <button
            key={src}
            onClick={() => onSourceToggle(src)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              enabledSources.includes(src)
                ? 'border-sky-500 bg-sky-500/10 text-sky-400'
                : 'border-gray-700 bg-gray-800/50 text-gray-600'
            }`}
          >
            {SOURCE_LABELS[src] ?? src}
          </button>
        ))}
      </div>
    </div>
  )
}
