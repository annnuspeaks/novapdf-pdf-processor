import { tools } from '../../tools';
import ToolWorkspace from '../../components/common/ToolWorkspace';

export default function ExtractText() {
  const tool = tools.find(item => item.slug === 'extract-text')!;
  return <ToolWorkspace tool={tool} />;
}
