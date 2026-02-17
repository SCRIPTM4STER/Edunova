import { useEffect, useState } from 'react'
import { notebookApi } from '../api/notebooks'
import { Alert } from '../components/Alert'
import { Loader } from '../components/Loader'

const initialNote = { title: '', content: '', notebook: '', is_public: false }

export const NotesPage = () => {
  const [notebooks, setNotebooks] = useState([])
  const [notes, setNotes] = useState([])
  const [form, setForm] = useState(initialNote)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  const loadData = async () => {
    setLoading(true)
    setError('')
    try {
      const [notebooksRes, notesRes] = await Promise.all([
        notebookApi.getNotebooks(),
        notebookApi.getNotes({ page_size: 20 }),
      ])
      setNotebooks(notebooksRes.data)
      setNotes(notesRes.data.results || [])
      if (notebooksRes.data.length && !form.notebook) {
        setForm((prev) => ({ ...prev, notebook: notebooksRes.data[0].id }))
      }
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to load notes.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const submitNote = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await notebookApi.createNote(form)
      setForm((prev) => ({ ...initialNote, notebook: prev.notebook }))
      await loadData()
    } catch (err) {
      setError(JSON.stringify(err?.response?.data || 'Failed to create note.'))
    }
  }

  const deleteNote = async (id) => {
    try {
      await notebookApi.deleteNote(id)
      await loadData()
    } catch {
      setError('Failed to delete note.')
    }
  }

  const generatePdf = async (id) => {
    try {
      await notebookApi.generatePdfFromNote(id)
      alert('PDF generated and saved in your PDF library.')
    } catch {
      setError('Failed to generate PDF from note.')
    }
  }

  if (loading) return <Loader text="Loading notes..." />

  return (
    <section>
      <h1>Notes</h1>
      <Alert message={error} />
      <div className="split">
        <form onSubmit={submitNote} className="panel">
          <h3>Create Note</h3>
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
            {notebooks.map((nb) => (
              <option key={nb.id} value={nb.id}>
                {nb.name}
              </option>
            ))}
          </select>
          <label className="row">
            <input
              type="checkbox"
              checked={form.is_public}
              onChange={(e) => setForm((prev) => ({ ...prev, is_public: e.target.checked }))}
            />
            Public note
          </label>
          <button>Create note</button>
        </form>
        <div className="panel">
          <h3>Note List</h3>
          <ul className="list">
            {notes.map((note) => (
              <li key={note.id}>
                <div>
                  <strong>{note.title}</strong>
                  <p className="muted">{note.notebook_name}</p>
                </div>
                <div className="row">
                  <button onClick={() => generatePdf(note.id)}>Generate PDF</button>
                  <button className="danger" onClick={() => deleteNote(note.id)}>
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
