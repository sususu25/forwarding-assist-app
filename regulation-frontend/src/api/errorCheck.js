import axios from "axios";
const api = axios.create({ baseURL: "/api/error-check" });

export const checkErrors = (payload) => api.post("/check-errors", payload); 