import { Link, NavLink, Outlet } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

export const AppLayout = () => {
  const { user, logout } = useAuth()

  return (
    <div className="app-shell">
      <header>
        <Link to="/" className="logo">
          EduNova
        </Link>
        <nav>
          <NavLink to="/dashboard">Dashboard</NavLink>
          <NavLink to="/notes">Notes</NavLink>
          <NavLink to="/pdfs">PDFs</NavLink>
          <NavLink to="/profile">Profile</NavLink>
        </nav>
        <div className="user-box">
          <span>{user?.user?.email || user?.user?.username}</span>
          <button onClick={logout}>Logout</button>
        </div>
      </header>
      <main>
        <Outlet />
      </main>
    </div>
  )
}
