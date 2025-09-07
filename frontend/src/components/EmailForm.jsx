import React, { useState, useRef } from 'react'

export default function EmailForm({ onSubmit, onClear, loading }) {
  const [text, setText] = useState('')
  const [file, setFile] = useState(null)

  // Cria referência para o input de arquivo
  const fileInputRef = useRef(null)


  function handleSubmit(e) {
    e.preventDefault()
    onSubmit({ text, file })
  }

  function handleClear() {
    setText('')
    setFile(null)
    onClear()
    // Limpa o input de arquivo
    if (fileInputRef.current) {
      fileInputRef.current.value = null
    }

  }

  return (
    <section className="card">
      <form onSubmit={handleSubmit}>
        <label>Colar texto do email</label>
        <textarea
          rows="8"
          value={text}
          disabled={loading}
          onChange={(e)=>setText(e.target.value)}
          placeholder="Cole aqui o conteúdo do email..."
        />

        <div className="row">
          <label>ou enviar arquivo (.pdf ou .txt)</label>
          <input
            type="file"
            accept=".pdf,text/plain"
            disabled={loading}
            onChange={(e)=>setFile(e.target.files[0])}
            ref={fileInputRef}
          />
        </div>

        <div className="actions">
          <button type="submit" disabled={loading}>
            {loading ? <span className="spinner"></span> : 'Processar'}
          </button>
          <button type="button" onClick={handleClear} disabled={loading}>
            Limpar
          </button>
        </div>
      </form>
    </section>
  )
}
