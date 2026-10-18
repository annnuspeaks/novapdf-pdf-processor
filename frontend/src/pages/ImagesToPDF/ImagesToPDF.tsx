import { tools } from '../../tools';
import ToolWorkspace from '../../components/common/ToolWorkspace';

export default function ImagesToPDF() {
  const tool = tools.find(item => item.slug === 'images-to-pdf')!;
  return <ToolWorkspace tool={tool} />;
}
