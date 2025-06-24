import axios from "axios";
const api = axios.create({ baseURL: "/api/generator" });

export const listDocs    = ()         => api.get("/documents");
export const generateDoc = (payload) => api.post("/generate-pdf", payload);
export const downloadDoc = (id)      => api.get(`/documents/${id}`, { responseType:"blob" });
export const deleteDoc   = (id)      => api.delete(`/documents/${id}`);
