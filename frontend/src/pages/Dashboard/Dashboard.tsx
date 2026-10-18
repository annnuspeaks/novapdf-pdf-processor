import { tools } from '../../tools';
import ToolGrid from '../../components/dashboard/ToolGrid';

export default function Dashboard() {
  return <section className="page dashboard-page">
    <div className="eyebrow">YOUR DOCUMENT WORKSPACE</div>
    <div className="hero-row"><div><h1>PDF tasks, <span>made simple.</span></h1><p className="intro">Everything you need for everyday PDF work, in one focused workspace.</p></div><div className="hero-stamp"><span>✳</span><small>Free to use<br/>No paid APIs</small></div></div>
    <div className="section-heading"><div><h2>Choose a tool</h2><p>Pick a tool to get started. Your workflow stays on one page.</p></div><span className="count-pill">{tools.length} TOOLS</span></div>
    <ToolGrid />
    <div className="privacy-note"><span className="shield">◇</span><div><strong>Built with privacy in mind</strong><p>Files will be processed only for the requested task, with temporary-file cleanup on the backend.</p></div><span className="note-tag">MVP PRINCIPLE</span></div>
  </section>;
}
