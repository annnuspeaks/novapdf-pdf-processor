import { Link } from 'react-router-dom';
export default function NotFound() { return <section className="page"><div className="eyebrow">404 / NOT FOUND</div><h1>Page not found.</h1><p className="intro">The page you requested does not exist.</p><Link className="back-link" to="/">← Back to dashboard</Link></section>; }
