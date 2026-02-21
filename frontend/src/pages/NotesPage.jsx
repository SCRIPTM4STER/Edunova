import { useEffect, useMemo, useState } from 'react'
import { notebookApi } from '../api/notebooks'
import { Alert } from '../components/Alert'
import { EmptyState } from '../components/EmptyState'
import { Loader } from '../components/Loader'
import { Pagination } from '../components/Pagination'

const initialForm = { title: '', content: '', notebook: '', is_public: false, image: null }

export const NotesPage = () => {
  const [notebooks, setNotebooks] = useState([])
  const [notes, setNotes] = useState([])
  const [listMeta, setListMeta] = useState({ count: 0, next: null, previous: null })
  const [page, setPage] = useState(1)
  const [form, setForm] = useState(initialForm)
  const [editingId, setEditingId] = useState(null)
  const [selectedNote, setSelectedNote] = useState(null)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const notebookOptions = useMemo(() => notebooks.map((nb) => ({ label: nb.name, value: nb.id })), [notebooks])

  const loadData = async (targetPage = page) => {
    setLoading(true)
    setError('')
    try {
      const [notebooksRes, notesRes] = await Promise.all([
        notebookApi.getNotebooks(),
        notebookApi.getNotes({ page: targetPage, page_size: 10 }),
      ])
      setNotebooks(notebooksRes.data)
      setNotes(notesRes.data.results || [])
      setListMeta({
        count: notesRes.data.count || 0,
        next: notesRes.data.next,
        previous: notesRes.data.previous,
      })

      if (!form.notebook && notebooksRes.data.length > 0) {
        setForm((prev) => ({ ...prev, notebook: notebooksRes.data[0].id }))
      }
    } catch (err) {
      setError(err?.response?.data?.detail || JSON.stringify(err?.response?.data) || 'Failed to load notes.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData(page)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page])

  const resetForm = () => {
    setForm((prev) => ({ ...initialForm, notebook: prev.notebook || notebookOptions[0]?.value || '' }))
    setEditingId(null)
  }

  const startEdit = async (noteId) => {
    setError('')
    const { data } = await notebookApi.getNote(noteId)
    setEditingId(noteId)
    setForm({
      title: data.title,
      content: data.content,
      notebook: data.notebook,
      is_public: data.is_public,
      image: null,
    })
  }

  const openDetails = async (noteId) => {
    setError('')
    try {
      const { data } = await notebookApi.getNote(noteId)
      setSelectedNote(data)
    } catch {
      setError('Could not load note details.')
    }
  }

  const submit = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    setError('')
    setSuccess('')

    try {
      if (editingId) {
        await notebookApi.updateNote(editingId, form)
        setSuccess('Note updated.')
      } else {
        await notebookApi.createNote(form)
        setSuccess('Note created.')
      }
      resetForm()
      await loadData(page)
    } catch (err) {
      setError(JSON.stringify(err?.response?.data || 'Unable to save note.'))
    } finally {
      setSubmitting(false)
    }
  }

  const deleteNote = async (id) => {
    if (!window.confirm('Delete this note?')) return
    try {
      await notebookApi.deleteNote(id)
      setSuccess('Note deleted.')
      await loadData(page)
    } catch {
      setError('Failed to delete note.')
    }
  }

  const generatePdf = async (id) => {
    setError('')
    setSuccess('')
    try {
      await notebookApi.generatePdfFromNote(id)
      setSuccess('PDF generated. Check PDF Library.')
    } catch {
      setError('Failed to generate PDF from note.')
    }
  }

  if (loading) return <Loader text="Loading notes..." />

  return (
    <section>
      <h1>Notes</h1>
      <Alert message={error} />
      <Alert type="info" message={success} />

      <div className="split">
        <form onSubmit={submit} className="panel">
          <h3>{editingId ? 'Edit Note' : 'Create Note'}</h3>
          <input
            placeholder="Title"
            value={form.title}
            onChange={(e) => setForm((prev) => ({ ...prev, title: e.target.value }))}
            required
          />
          <textarea
            placeholder="Content"
            value={form.content}
            onChange={(e) => setForm((prev) => ({ ...prev, content: e.target.value }))}
            required
          />
          <select
            value={form.notebook}
            onChange={(e) => setForm((prev) => ({ ...prev, notebook: e.target.value }))}
            required
          >
            {notebookOptions.map((nb) => (
              <option key={nb.value} value={nb.value}>
                {nb.label}
              </option>
            ))}
          </select>
          <label className="field">
            <span>Optional image</span>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setForm((prev) => ({ ...prev, image: e.target.files?.[0] || null }))}
            />
          </label>
          <label className="row">
            <input
              type="checkbox"
              checked={form.is_public}
              onChange={(e) => setForm((prev) => ({ ...prev, is_public: e.target.checked }))}
            />
            Public note
          </label>
          <div className="row">
            <button disabled={submitting}>{submitting ? 'Saving...' : editingId ? 'Save changes' : 'Create note'}</button>
            {editingId ? (
              <button type="button" className="secondary" onClick={resetForm}>
                Cancel
              </button>
            ) : null}
          </div>
        </form>

        <div className="panel">
          <h3>Note List</h3>
          {notes.length === 0 ? (
            <EmptyState title="No notes yet" subtitle="Create your first note to get started." />
          ) : (
            <ul className="list">
              {notes.map((note) => (
                <li key={note.id}>
                  <div>
                    <strong>{note.title}</strong>
                    <p className="muted">{note.notebook_name}</p>
                  </div>
                  <div className="row wrap">
                    <button onClick={() => openDetails(note.id)}>View</button>
                    <button onClick={() => startEdit(note.id)}>Edit</button>
                    <button onClick={() => generatePdf(note.id)}>Generate PDF</button>
                    <button className="danger" onClick={() => deleteNote(note.id)}>
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

      {selectedNote ? (
        <div className="panel detail-panel">
          <div className="row space-between">
            <h3>{selectedNote.title}</h3>
            <button className="secondary" onClick={() => setSelectedNote(null)}>
              Close
            </button>
          </div>
          <p>{selectedNote.content}</p>
          {selectedNote.image ? <img src={selectedNote.image} alt={selectedNote.title} className="preview-image" /> : null}
          <p className="muted">Updated: {new Date(selectedNote.updated_at).toLocaleString()}</p>
        </div>
      ) : null}
    </section>
  )
}
