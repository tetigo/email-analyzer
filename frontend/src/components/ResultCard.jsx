import React from 'react'

export default function ResultCard({ result, loading }) {
  if (loading) {
    return (
      <div className="result skeleton">
        <div className="skeleton-line w-1/3"></div>
        <div className="skeleton-line w-2/3"></div>
        <div className="skeleton-block"></div>
      </div>
    )
  }

  if (!result) return null

  return (
    <div className="result">
      <h3>Resultado</h3>
      <p>
        <strong>Categoria:</strong> {result.category}
        {result.confidence ? ` (${(result.confidence*100).toFixed(0)}%)` : ''}
      </p>

      <h4>Resposta sugerida</h4>
      <pre className="suggestion">{result.suggested_response}</pre>

      <div className="small-actions">
        <button onClick={() => navigator.clipboard.writeText(result.suggested_response)}>
          Copiar resposta
        </button>
        <button onClick={() => {
          const blob = new Blob([result.suggested_response], {type:'text/plain;charset=utf-8'})
          const url = URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = url
          a.download = 'resposta.txt'
          a.click()
          URL.revokeObjectURL(url)
        }}>
          Baixar .txt
        </button>
      </div>
    </div>
  )
}
