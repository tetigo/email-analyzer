import React, { useState } from 'react'
import EmailForm from './components/EmailForm'
import ResultCard from './components/ResultCard'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function App() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  async function handleProcess({ text, file }) {
    setError(null)
    setResult(null)
    if (!text && !file) { setError('⚠️ Cole o texto do email ou faça upload de um arquivo.'); return }
    setLoading(true)
    try {
      const fd = new FormData()
      if (file) fd.append('file', file)
      if (text) fd.append('text', text)
      const res = await fetch(`${API_URL}/api/process-email`, {
        method: 'POST',
        body: fd
      })
      if (!res.ok) throw new Error(await res.text())
      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError(err.message || 'Erro desconhecido')
    } finally {
      setLoading(false)
    }
  }

  function handleClear() {
    setError(null)
    setResult(null)
    setLoading(false)
  }

  return (
    <div className="app">
      <header className="header">
        <h1>AutoU — Classificador de Emails</h1>
        <p className="subtitle">Faça upload de um .txt ou .pdf, ou cole o texto. O sistema sugerirá categoria e resposta.</p>
      </header>
      <main>
        <EmailForm onSubmit={handleProcess} loading={loading} onClear={handleClear} />
        {error && <div className="error-box">{error}</div>}
        {(loading || result) && <ResultCard result={result} loading={loading} />}
      </main>
      <footer className="footer">
        <small>Feito para o case AutoU • Tiago Mendes</small>
      </footer>
    </div>
  )
}
