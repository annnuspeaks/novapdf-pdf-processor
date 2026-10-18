import { Link } from 'react-router-dom';
import FileUpload from './FileUpload';
import type { Tool } from '../../tools';

export default function ToolWorkspace({ tool }: { tool: Tool }) {
  return <section className="page tool-page">
    <Link to="/" className="back-link">← All tools</Link>
    <div className="eyebrow">PDF WORKSPACE / TOOL</div>
    <div className="tool-title-row"><div><h1>{tool.title}</h1><p className="intro">{tool.description}</p></div><div className="tool-icon large">{tool.icon}</div></div>
    <div className="work-panel">
      <div className="panel-heading"><div><h2>Start with your file</h2><p>Choose your file to prepare the task. Processing activates when the backend is connected.</p></div><span className="step-pill">STEP 01</span></div>
      <FileUpload tool={tool} />
      <div className="notice"><span>ⓘ</span><p>Frontend foundation is ready. File processing will be enabled after the FastAPI endpoints are implemented in the backend phase.</p></div>
      <button className="primary-button" type="button" disabled>Backend connection pending <span>→</span></button>
    </div>
    <div className="workflow-strip"><div><span>01</span><strong>Upload</strong><small>Select your file(s)</small></div><i>→</i><div><span>02</span><strong>Process</strong><small>Backend validation</small></div><i>→</i><div><span>03</span><strong>Download</strong><small>Get your result</small></div></div>
  </section>;
}
