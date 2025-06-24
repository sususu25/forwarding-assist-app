import axios from "axios";
const api = axios.create({ baseURL: "/api/regulation" });

export const getRegulationInfo = (params) => api.get("/info", { params }); 