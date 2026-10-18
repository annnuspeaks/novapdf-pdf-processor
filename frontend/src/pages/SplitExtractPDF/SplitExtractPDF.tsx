import { tools } from '../../tools';
import ToolWorkspace from '../../components/common/ToolWorkspace';

export default function SplitExtractPDF() {
  const tool = tools.find(item => item.slug === 'split-extract-pdf')!;
  return <ToolWorkspace tool={tool} />;
}
