const COLORS: Record<string, string> = {
  yts:     'bg-yellow-500/10 text-yellow-400 border-yellow-500/30',
  nyaa:    'bg-purple-500/10 text-purple-400 border-purple-500/30',
  eztv:    'bg-blue-500/10   text-blue-400   border-blue-500/30',
  '1337x': 'bg-green-500/10  text-green-400  border-green-500/30',
  tpb:     'bg-red-500/10    text-red-400    border-red-500/30',
  rarbg:   'bg-orange-500/10 text-orange-400 border-orange-500/30',
}
const LABELS: Record<string, string> = {
  yts: 'YTS', nyaa: 'Nyaa', eztv: 'EZTV', '1337x': '1337x', tpb: 'TPB', rarbg: 'RARBG',
}

export function SourceBadge({ source }: { source: string }) {
  const cls = COLORS[source] ?? 'bg-gray-700 text-gray-400 border-gray-600'
  return (
    <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${cls}`}>
      {LABELS[source] ?? source}
    </span>
  )
}
