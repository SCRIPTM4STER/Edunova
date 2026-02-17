import { useEffect, useState } from 'react'
import { notebookApi } from '../api/notebooks'
import { pdfApi } from '../api/pdfs'
import { Alert } from '../components/Alert'
import { Loader } from '../components/Loader'

export const DashboardPage = () => {
  const [stats, setStats] = useState({ notebooks: 0, notes: 0, pdfs: 0 })
  const [notebooks, setNotebooks] = useState([])
  const [newNotebook, setNewNotebook] = useState({ name: '', description: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  const fetchSummary = async () => {
    const [notebooksRes, notesRes, pdfsRes] = await Promise.all([
      notebookApi.getNotebooks(),
      notebookApi.getNotes(),
      pdfApi.listPdfs(),
    ])
    setNotebooks(notebooksRes.data)
    setStats({
      notebooks: notebooksRes.data.length,
      notes: notesRes.data.count || notesRes.data.results?.length || 0,
      pdfs: pdfsRes.data.count || pdfsRes.data.results?.length || 0,
    })
  }

  useEffect(() => {
    fetchSummary()
      .catch(() => setError('Failed to load dashboard data.'))
      .finally(() => setLoading(false))
  }, [])

  const createNotebook = async (e) => {
    e.preventDefault()
    await notebookApi.createNotebook(newNotebook)
    setNewNotebook({ name: '', description: '' })
    await fetchSummary()
  }

  if (loading) return <Loader text="Loading dashboard..." />

  return (
    <section>
      <h1>Dashboard</h1>
      <Alert message={error} />
      <div className="cards">
        <article className="card">
          <h3>Notebooks</h3>
          <p>{stats.notebooks}</p>
        </article>
        <article className="card">
          <h3>Notes</h3>
          <p>{stats.notes}</p>
        </article>
        <article className="card">
          <h3>PDFs</h3>
          <p>{stats.pdfs}</p>
        </article>
      </div>
      <div className="split">
        <form className="panel" onSubmit={createNotebook}>
          <h3>Create Notebook</h3>
          <input
            placeholder="Notebook name"
            value={newNotebook.name}
            onChange={(e) => setNewNotebook((prev) => ({ ...prev, name: e.target.value }))}
            required
          />
          <textarea
            placeholder="Description"
            value={newNotebook.description}
            onChange={(e) => setNewNotebook((prev) => ({ ...prev, description: e.target.value }))}
          />
          <button>Create</button>
        </form>
        <div className="panel">
          <h3>Notebook List</h3>
          <ul className="list">
            {notebooks.map((notebook) => (
              <li key={notebook.id}>
                <div>
                  <strong>{notebook.name}</strong>
                  <p className="muted">{notebook.description || 'No description'}</p>
                </div>
                <span>{notebook.notes_count} notes</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  )
}
