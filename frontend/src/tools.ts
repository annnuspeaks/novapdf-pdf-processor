export type Tool = {
  slug: string;
  title: string;
  description: string;
  icon: string;
  formats: string;
  endpoint: string;
  mode?: 'single' | 'multiple';
  accept?: string;
};

export const tools: Tool[] = [
  {
    slug: 'images-to-pdf',
    title: 'Images to PDF',
    description: 'Turn JPG or PNG images into one clean PDF.',
    icon: '▧',
    formats: 'JPG · PNG → PDF',
    endpoint: '/api/tools/images-to-pdf',
    mode: 'multiple',
    accept: 'image/jpeg,image/png',
  },
  {
    slug: 'merge-pdfs',
    title: 'Merge PDFs',
    description: 'Combine multiple PDF files in the order you choose.',
    icon: '⇢',
    formats: 'PDF + PDF → PDF',
    endpoint: '/api/tools/merge-pdfs',
    mode: 'multiple',
    accept: 'application/pdf,.pdf',
  },
  {
    slug: 'split-extract-pdf',
    title: 'Split / Extract Pages',
    description: 'Create smaller PDFs from the page ranges you need.',
    icon: '⤢',
    formats: 'PDF → PDF / ZIP',
    endpoint: '/api/tools/split-pdf',
    mode: 'single',
    accept: 'application/pdf,.pdf',
  },
  {
    slug: 'rotate-pdf',
    title: 'Rotate PDF Pages',
    description: 'Rotate all pages or selected pages by 90° increments.',
    icon: '⟳',
    formats: 'PDF → PDF',
    endpoint: '/api/tools/rotate-pdf',
    mode: 'single',
    accept: 'application/pdf,.pdf',
  },
  {
    slug: 'extract-text',
    title: 'Extract Text',
    description: 'Export selectable PDF text to a plain-text file.',
    icon: 'T',
    formats: 'PDF → TXT',
    endpoint: '/api/tools/extract-text',
    mode: 'single',
    accept: 'application/pdf,.pdf',
  },
];
