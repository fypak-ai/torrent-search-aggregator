import { Copy, Download } from 'lucide-react'
import type { TorrentResult } from '../lib/api'
import { SourceBadge } from './SourceBadge'

interface Props { result: TorrentResult }

export function ResultCard({ result }: Props) {
  const copy = () => navigator.clipboard.writeText(result.magnet)
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-lg p-4 hover:border-gray-700 transition-colors">
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <SourceBadge source={result.source_id} />
            {result.category && (
              <span className="text-xs text-gray-500 capitalize">{result.category}</span>
            )}
          </div>
          <h3 className="text-sm font-medium text-white truncate">{result.title}</h3>
          <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
            {result.size && <span>{result.size}</span>}
            {result.seeders > 0 && (
              <span className="text-green-400 flex items-center gap-1">
                <span className="w-1.5 h-1.5 bg-green-400 rounded-full inline-block" />
                {result.seeders} seeds
              </span>
            )}
            {result.leechers > 0 && (
              <span className="text-red-400">{result.leechers} peers</span>
            )}
          </div>
        </div>
        <div className="flex gap-2 shrink-0">
          <button
            onClick={copy}
            title="Copiar magnet"
            className="p-2 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-400 hover:text-white transition-colors"
          >
            <Copy className="w-4 h-4" />
          </button>
          <a
            href={result.magnet}
            title="Abrir magnet"
            className="p-2 rounded-lg bg-sky-600/20 hover:bg-sky-600/40 text-sky-400 hover:text-sky-300 transition-colors"
          >
            <Download className="w-4 h-4" />
          </a>
        </div>
      </div>
    </div>
  )
}
