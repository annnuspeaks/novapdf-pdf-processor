import { tools } from '../../tools';
import ToolWorkspace from '../../components/common/ToolWorkspace';

export default function MergePDF() {
  const tool = tools.find(item => item.slug === 'merge-pdfs')!;
  return <ToolWorkspace tool={tool} />;
}
