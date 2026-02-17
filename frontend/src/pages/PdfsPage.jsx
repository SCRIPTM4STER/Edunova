import { useEffect, useState } from 'react'
import { pdfApi } from '../api/pdfs'
import { Alert } from '../components/Alert'
import { Loader } from '../components/Loader'

export const PdfsPage = () => {
  const [pdfs, setPdfs] = useState([])
  const [file, setFile] = useState(null)
  const [form, setForm] = useState({ file_name: '', title: '', description: '', is_public: false })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  const load = async () => {
    setLoading(true)
    try {
      const { data } = await pdfApi.listPdfs({ page_size: 20 })
      setPdfs(data.results || [])
    } catch {
      setError('Failed to load PDFs.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  const upload = async (e) => {
    e.preventDefault()
    if (!file) return
    const data = new FormData()
    data.append('file', file)
    data.append('file_name', form.file_name || file.name)
    data.append('title', form.title)
    data.append('description', form.description)
    data.append('is_public', form.is_public)

    try {
      await pdfApi.uploadPdf(data)
      setFile(null)
      setForm({ file_name: '', title: '', description: '', is_public: false })
      await load()
    } catch (err) {
      setError(JSON.stringify(err?.response?.data || 'Upload failed'))
    }
  }

  const download = async (pdf) => {
    const { data } = await pdfApi.downloadPdf(pdf.id)
    const url = window.URL.createObjectURL(data)
    const a = document.createElement('a')
    a.href = url
    a.download = pdf.file_name || 'download.pdf'
    a.click()
    window.URL.revokeObjectURL(url)
  }

  const remove = async (id) => {
    await pdfApi.deletePdf(id)
    await load()
  }

  if (loading) return <Loader text="Loading PDFs..." />

  return (
    <section>
      <h1>PDF Library</h1>
      <Alert message={error} />
      <div className="split">
        <form className="panel" onSubmit={upload}>
          <h3>Upload PDF</h3>
          <input type="file" accept="application/pdf" onChange={(e) => setFile(e.target.files?.[0] || null)} required />
          <input
            placeholder="File name"
            value={form.file_name}
            onChange={(e) => setForm((prev) => ({ ...prev, file_name: e.target.value }))}
          />
          <input
            placeholder="Title"
            value={form.title}
            onChange={(e) => setForm((prev) => ({ ...prev, title: e.target.value }))}
          />
          <textarea
            placeholder="Description"
            value={form.description}
            onChange={(e) => setForm((prev) => ({ ...prev, description: e.target.value }))}
          />
          <label className="row">
            <input
              type="checkbox"
              checked={form.is_public}
              onChange={(e) => setForm((prev) => ({ ...prev, is_public: e.target.checked }))}
            />
            Public PDF
          </label>
          <button>Upload</button>
        </form>
        <div className="panel">
          <h3>My PDFs</h3>
          <ul className="list">
            {pdfs.map((pdf) => (
              <li key={pdf.id}>
                <div>
                  <strong>{pdf.file_name}</strong>
                  <p className="muted">{pdf.title || 'Untitled'}</p>
                </div>
                <div className="row">
                  <button onClick={() => download(pdf)}>Download</button>
                  <button className="danger" onClick={() => remove(pdf.id)}>
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  )
}
