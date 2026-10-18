import { tools } from '../../tools';
import ToolCard from './ToolCard';

export default function ToolGrid() {
  return <div className="tool-grid">{tools.map((tool, index) => <ToolCard key={tool.slug} tool={tool} index={index} />)}</div>;
}
