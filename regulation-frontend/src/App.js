import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import RegulationPage from "./components/RegulationPage";
import DocEditor from "./components/DocEditor";
import DocumentsPage from "./DocumentsPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<RegulationPage />} />
          <Route path="/docs" element={<DocumentsPage />} />
          <Route path="/docs/create" element={<DocEditor />} />
          <Route path="/settings" element={<div style={{padding:40}}>Settings</div>} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
