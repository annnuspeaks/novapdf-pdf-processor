import { Link } from 'react-router-dom';
import { tools } from '../../tools';

export default function Footer() {
  return <footer className="site-footer">
    <div className="footer-main">
      <div className="footer-brand-block">
        <Link to="/" className="footer-logo-link" aria-label="NOVA PDF home"><img src="/images/nova-pdf-logo.png" alt="NOVA PDF" className="footer-logo" /></Link>
        <p>Free PDF tools for everyday document tasks. Simple workflows, clear results.</p>
      </div>
      <div className="footer-column"><h3>PDF TOOLS</h3>{tools.slice(0,3).map(t => <Link key={t.slug} to={`/tools/${t.slug}`}>{t.title}</Link>)}</div>
      <div className="footer-column"><h3>MORE TOOLS</h3>{tools.slice(3).map(t => <Link key={t.slug} to={`/tools/${t.slug}`}>{t.title}</Link>)}</div>
      <div className="footer-column"><h3>OUR PROMISE</h3><span>Free to use</span><span>No paid APIs</span><span>Privacy-conscious workflow</span></div>
    </div>
    <div className="footer-bottom"><span>© {new Date().getFullYear()} NOVA PDF. All rights reserved.</span><span>Simple tools. Clear workflow. Your files, handled carefully.</span></div>
  </footer>;
}
