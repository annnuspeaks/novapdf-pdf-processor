import { Route, Routes } from 'react-router-dom';
import AppLayout from '../components/layout/AppLayout';
import Dashboard from '../pages/Dashboard/Dashboard';
import ImagesToPDF from '../pages/ImagesToPDF/ImagesToPDF';
import MergePDF from '../pages/MergePDF/MergePDF';
import SplitExtractPDF from '../pages/SplitExtractPDF/SplitExtractPDF';
import RotatePDF from '../pages/RotatePDF/RotatePDF';
import ExtractText from '../pages/ExtractText/ExtractText';
import NotFound from '../pages/NotFound/NotFound';

export default function AppRoutes() {
  return <Routes><Route element={<AppLayout />}>
    <Route path="/" element={<Dashboard />} />
    <Route path="/tools/images-to-pdf" element={<ImagesToPDF />} />
    <Route path="/tools/merge-pdfs" element={<MergePDF />} />
    <Route path="/tools/split-extract-pdf" element={<SplitExtractPDF />} />
    <Route path="/tools/rotate-pdf" element={<RotatePDF />} />
    <Route path="/tools/extract-text" element={<ExtractText />} />
    <Route path="*" element={<NotFound />} />
  </Route></Routes>;
}
