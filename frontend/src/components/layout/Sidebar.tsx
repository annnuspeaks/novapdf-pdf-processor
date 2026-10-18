import { NavLink, Link } from 'react-router-dom';
import { tools } from '../../tools';

export default function Sidebar() {
  return <aside className="sidebar">
    <Link to="/" className="brand" aria-label="NOVA PDF home">
      <img className="brand-logo" src="/images/nova-pdf-logo.png" alt="NOVA PDF" />
    </Link>
    <p className="nav-label">WORKSPACE</p>
    <NavLink to="/" end className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}><span>▦</span> Dashboard</NavLink>
    <p className="nav-label tools-label">YOUR TOOLS</p>
    {tools.map(tool => <NavLink key={tool.slug} to={`/tools/${tool.slug}`} className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}><span>{tool.icon}</span>{tool.title}</NavLink>)}
    <div className="sidebar-bottom"><span className="status-dot" /> Free tools · No paid APIs</div>
  </aside>;
}
