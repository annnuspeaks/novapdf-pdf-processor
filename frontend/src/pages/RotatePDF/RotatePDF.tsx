import { tools } from '../../tools';
import ToolWorkspace from '../../components/common/ToolWorkspace';

export default function RotatePDF() {
  const tool = tools.find(item => item.slug === 'rotate-pdf')!;
  return <ToolWorkspace tool={tool} />;
}
