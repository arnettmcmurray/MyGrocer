import api from "./axios";

export const getHouseholds = () => api.get("/api/v1/households");
export const getHousehold = (id) => api.get(`/api/v1/households/${id}`);
export const createHousehold = (data) => api.post("/api/v1/households", data);
export const updateHousehold = (id, data) =>
  api.put(`/api/v1/households/${id}`, data);
export const deleteHousehold = (id) => api.delete(`/api/v1/households/${id}`);
