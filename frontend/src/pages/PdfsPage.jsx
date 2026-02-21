import { useEffect, useState } from 'react'
import { notebookApi } from '../api/notebooks'
import { pdfApi } from '../api/pdfs'
import { Alert } from '../components/Alert'
import { EmptyState } from '../components/EmptyState'
import { Loader } from '../components/Loader'
import { Pagination } from '../components/Pagination'

const initialForm = {
  file_name: '',
  title: '',
  description: '',
  is_public: false,
  linked_note: '',
  file: null,
  cover_image: null,
}

export const PdfsPage = () => {
  const [pdfs, setPdfs] = useState([])
  const [notes, setNotes] = useState([])
  const [form, setForm] = useState(initialForm)
  const [listMeta, setListMeta] = useState({ count: 0, next: null, previous: null })
  const [page, setPage] = useState(1)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [editingPdf, setEditingPdf] = useState(null)
  const [selectedPdf, setSelectedPdf] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const load = async (targetPage = page) => {
    setLoading(true)
    setError('')
    try {
      const [pdfRes, noteRes] = await Promise.all([
        pdfApi.listPdfs({ page: targetPage, page_size: 10 }),
        notebookApi.getNotes({ page: 1, page_size: 50 }),
      ])
      setPdfs(pdfRes.data.results || [])
      setListMeta({ count: pdfRes.data.count, next: pdfRes.data.next, previous: pdfRes.data.previous })
      setNotes(noteRes.data.results || [])
    } catch {
      setError('Failed to load PDFs.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load(page)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page])

  const onUpload = async (e) => {
    e.preventDefault()
    if (!form.file && !editingPdf) {
      setError('PDF file is required for upload.')
      return
    }

    setError('')
    setSuccess('')
    const payload = { ...form }
    if (!payload.linked_note) delete payload.linked_note

    if (form.file && form.file.size > 10 * 1024 * 1024) {
      setError('PDF must be 10MB or less.')
      return
    }

    try {
      if (editingPdf) {
        await pdfApi.updatePdf(editingPdf.id, payload)
        setSuccess('PDF updated.')
      } else {
        await pdfApi.uploadPdf(payload, (event) => {
          if (!event.total) return
          setUploadProgress(Math.round((event.loaded * 100) / event.total))
        })
        setSuccess('PDF uploaded.')
      }
      setForm(initialForm)
      setEditingPdf(null)
      setUploadProgress(0)
      await load(page)
    } catch (err) {
      setError(JSON.stringify(err?.response?.data || 'Upload failed'))
    }
  }

  const startEdit = async (pdfId) => {
    const { data } = await pdfApi.getPdf(pdfId)
    setEditingPdf(data)
    setForm({
      ...initialForm,
      file_name: data.file_name || '',
      title: data.title || '',
      description: data.description || '',
      is_public: Boolean(data.is_public),
      linked_note: data.linked_note || '',
    })
  }

  const openDetails = async (pdfId) => {
    try {
      const { data } = await pdfApi.getPdf(pdfId)
      setSelectedPdf(data)
    } catch {
      setError('Could not load PDF details.')
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
    if (!window.confirm('Delete this PDF?')) return
    await pdfApi.deletePdf(id)
    setSuccess('PDF deleted.')
    await load(page)
  }

  if (loading) return <Loader text="Loading PDFs..." />

  return (
    <section>
      <h1>PDF Library</h1>
      <Alert message={error} />
      <Alert type="info" message={success} />
      <div className="split">
        <form className="panel" onSubmit={onUpload}>
          <h3>{editingPdf ? 'Edit PDF metadata' : 'Upload PDF'}</h3>
          <input
            type="file"
            accept="application/pdf"
            onChange={(e) => setForm((prev) => ({ ...prev, file: e.target.files?.[0] || null }))}
            required={!editingPdf}
          />
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
          <label className="field">
            <span>Cover image</span>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setForm((prev) => ({ ...prev, cover_image: e.target.files?.[0] || null }))}
            />
          </label>
          <select
            value={form.linked_note}
            onChange={(e) => setForm((prev) => ({ ...prev, linked_note: e.target.value }))}
          >
            <option value="">No linked note</option>
            {notes.map((note) => (
              <option key={note.id} value={note.id}>
                {note.title}
              </option>
            ))}
          </select>
          <label className="row">
            <input
              type="checkbox"
              checked={form.is_public}
              onChange={(e) => setForm((prev) => ({ ...prev, is_public: e.target.checked }))}
            />
            Public PDF
          </label>
          {!editingPdf && uploadProgress > 0 ? <p className="muted">Upload: {uploadProgress}%</p> : null}
          <div className="row">
            <button>{editingPdf ? 'Save changes' : 'Upload'}</button>
            {editingPdf ? (
              <button type="button" className="secondary" onClick={() => setEditingPdf(null)}>
                Cancel
              </button>
            ) : null}
          </div>
        </form>

        <div className="panel">
          <h3>PDFs</h3>
          {pdfs.length === 0 ? (
            <EmptyState title="No PDFs yet" subtitle="Upload or generate one from your notes." />
          ) : (
            <ul className="list">
              {pdfs.map((pdf) => (
                <li key={pdf.id}>
                  <div>
                    <strong>{pdf.file_name}</strong>
                    <p className="muted">{pdf.title || 'Untitled'}</p>
                  </div>
                  <div className="row wrap">
                    <button onClick={() => openDetails(pdf.id)}>View</button>
                    <button onClick={() => startEdit(pdf.id)}>Edit</button>
                    <button onClick={() => download(pdf)}>Download</button>
                    <button className="danger" onClick={() => remove(pdf.id)}>
                      Delete
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
          <Pagination
            page={page}
            total={listMeta.count}
            canPrev={Boolean(listMeta.previous)}
            canNext={Boolean(listMeta.next)}
            onPrev={() => setPage((prev) => Math.max(prev - 1, 1))}
            onNext={() => setPage((prev) => prev + 1)}
          />
        </div>
      </div>

      {selectedPdf ? (
        <div className="panel detail-panel">
          <div className="row space-between">
            <h3>{selectedPdf.file_name}</h3>
            <button className="secondary" onClick={() => setSelectedPdf(null)}>
              Close
            </button>
          </div>
          <p className="muted">Title: {selectedPdf.title || '-'}</p>
          <p>{selectedPdf.description || 'No description.'}</p>
          {selectedPdf.cover_image ? (
            <img src={selectedPdf.cover_image} alt={selectedPdf.file_name} className="preview-image" />
          ) : null}
          <p className="muted">Updated: {new Date(selectedPdf.updated_at).toLocaleString()}</p>
        </div>
      ) : null}
    </section>
  )
}
