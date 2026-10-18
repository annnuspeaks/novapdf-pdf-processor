import { Link } from 'react-router-dom';
import type { Tool } from '../../tools';

export default function ToolCard({ tool, index }: { tool: Tool; index: number }) {
  return <Link to={`/tools/${tool.slug}`} className="tool-card">
    <div className="card-top"><div className={`tool-icon icon-${index}`}>{tool.icon}</div><span className="arrow">↗</span></div>
    <h3>{tool.title}</h3><p>{tool.description}</p>
    <div className="card-bottom"><span>{tool.formats}</span><span className="open-label">Open tool →</span></div>
  </Link>;
}
