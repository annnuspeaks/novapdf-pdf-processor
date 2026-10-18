import { useLocation } from 'react-router-dom';
import { tools } from '../../tools';

export default function Header() {
  const { pathname } = useLocation();
  const tool = tools.find(item => pathname === `/tools/${item.slug}`);
  return <header className="topbar">
    <div className="breadcrumb"><span>Workspace</span><i>/</i><span>{tool?.title ?? 'PDF Utilities'}</span></div>
    <span className="free-badge">FREE WORKSPACE</span>
  </header>;
}
