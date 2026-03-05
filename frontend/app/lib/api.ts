import axios from 'axios'

const BASE = (import.meta.env.VITE_API_URL as string) ?? '/api'

export interface TorrentResult {
  title: string
  magnet: string
  size: string
  seeders: number
  leechers: number
  source: string
  source_id: string
  category: string
  date: string
  cover?: string
  rating?: string | number
  imdb?: string
}

export interface SearchResponse {
  query: string
  total: number
  results: TorrentResult[]
}

export async function searchTorrents(
  query: string,
  category = 'all',
  sources: string[] = [],
): Promise<SearchResponse> {
  const params: Record<string, string> = { q: query, category }
  if (sources.length > 0) params.sources = sources.join(',')
  const { data } = await axios.get<SearchResponse>(`${BASE}/search`, { params })
  return data
}

export async function getSources() {
  const { data } = await axios.get(`${BASE}/sources`)
  return data
}
