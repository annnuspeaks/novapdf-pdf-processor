import { useRef, useState } from 'react';
import type { ChangeEvent, DragEvent } from 'react';
import type { Tool } from '../../tools';

export default function FileUpload({ tool }: { tool: Tool }) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [files, setFiles] = useState<File[]>([]);
  const [dragging, setDragging] = useState(false);
  const multiple = tool.mode === 'multiple';
  const update = (list: FileList | null) => setFiles(list ? Array.from(list) : []);
  const onChange = (event: ChangeEvent<HTMLInputElement>) => update(event.currentTarget.files);
  const onDrop = (event: DragEvent<HTMLLabelElement>) => {
    event.preventDefault(); setDragging(false);
    const dropped = Array.from(event.dataTransfer.files);
    setFiles(multiple ? dropped : dropped.slice(0, 1));
  };
  const removeFile = (index: number) => setFiles(current => current.filter((_, i) => i !== index));
  return <>
    <label className={`drop-zone ${dragging ? 'is-dragging' : ''}`} onDragOver={e => {e.preventDefault(); setDragging(true);}} onDragLeave={() => setDragging(false)} onDrop={onDrop}>
      <input ref={inputRef} className="file-input-hidden" type="file" multiple={multiple} accept={tool.accept} onChange={onChange} />
      <span className="upload-icon">↑</span>
      <strong>{dragging ? 'Drop your file here' : `Drop ${multiple ? 'files' : 'a file'} here or browse`}</strong>
      <span className="muted">Supported: {tool.formats}</span>
      <button className="browse-button" type="button" onClick={() => inputRef.current?.click()}>Browse files</button>
    </label>
    {files.length === 0 ? <p className="selected-files">No files selected</p> : <div className="file-list" aria-live="polite">
      {files.map((file, index) => <div className="file-item" key={`${file.name}-${file.lastModified}-${index}`}><span className="file-type">{file.type.startsWith('image/') ? 'IMG' : 'PDF'}</span><div className="file-details"><strong>{file.name}</strong><small>{(file.size / (1024 * 1024)).toFixed(2)} MB</small></div><button className="remove-file" type="button" onClick={() => removeFile(index)} aria-label={`Remove ${file.name}`}>Remove</button></div>)}
      <button type="button" className="replace-files" onClick={() => inputRef.current?.click()}>Replace selection</button>
    </div>}
  </>;
}
