/**
 * EnQue API Service Client
 * Provides organized, typed service methods mapping cleanly to backend routes.
 */

const API_BASE = import.meta.env.VITE_API_URL || (import.meta.env.PROD ? "/api" : "http://localhost:8000/api");

function getAuthHeaders() {
  const token = localStorage.getItem("enque_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function handleResponse(res) {
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(errorData.detail || `Request failed with HTTP status ${res.status}`);
  }
  return res.json();
}

export const api = {
  // Authentication
  auth: {
    register: (name, email, password) =>
      fetch(`${API_BASE}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      }).then(handleResponse),

    login: (email, password) =>
      fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      }).then(handleResponse),

    me: () =>
      fetch(`${API_BASE}/auth/me`, {
        headers: { ...getAuthHeaders() },
      }).then(handleResponse),
  },

  // Brands
  brands: {
    list: () =>
      fetch(`${API_BASE}/brands`, {
        headers: { ...getAuthHeaders() },
      }).then(handleResponse),

    create: (brandData) =>
      fetch(`${API_BASE}/brands`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...getAuthHeaders() },
        body: JSON.stringify(brandData),
      }).then(handleResponse),

    get: (id) =>
      fetch(`${API_BASE}/brands/${id}`, {
        headers: { ...getAuthHeaders() },
      }).then(handleResponse),
  },

  // Data Ingestion
  data: {
    upload: (brandId, file, datasetType = "auto") => {
      const formData = new FormData();
      formData.append("brand_id", brandId);
      formData.append("dataset_type", datasetType);
      formData.append("file", file);

      return fetch(`${API_BASE}/data/upload`, {
        method: "POST",
        headers: { ...getAuthHeaders() },
        body: formData,
      }).then(handleResponse);
    },

    listFiles: (brandId) =>
      fetch(`${API_BASE}/data/files?brand_id=${brandId}`, {
        headers: { ...getAuthHeaders() },
      }).then(handleResponse),
  },

  // Content Analytics
  content: {
    getAnalytics: (brandId) =>
      fetch(`${API_BASE}/content/analytics?brand_id=${brandId}`, {
        headers: { ...getAuthHeaders() },
      }).then(handleResponse),

    getTopPerforming: (brandId, limit = 5) =>
      fetch(`${API_BASE}/content/top-performing?brand_id=${brandId}&limit=${limit}`, {
        headers: { ...getAuthHeaders() },
      }).then(handleResponse),

    getUnderperforming: (brandId, limit = 5) =>
      fetch(`${API_BASE}/content/underperforming?brand_id=${brandId}&limit=${limit}`, {
        headers: { ...getAuthHeaders() },
      }).then(handleResponse),
  },

  // Audience Intelligence
  audience: {
    getInsights: (brandId) =>
      fetch(`${API_BASE}/audience/insights?brand_id=${brandId}`, {
        headers: { ...getAuthHeaders() },
      }).then(handleResponse),

    getTrends: (brandId) =>
      fetch(`${API_BASE}/audience/trends?brand_id=${brandId}`, {
        headers: { ...getAuthHeaders() },
      }).then(handleResponse),
  },

  // Agents & Orchestrator
  agents: {
    generateStrategy: (brandId, query) =>
      fetch(`${API_BASE}/agents/strategy`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...getAuthHeaders() },
        body: JSON.stringify({ brand_id: brandId, query }),
      }).then(handleResponse),

    chat: (brandId, message) =>
      fetch(`${API_BASE}/agents/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...getAuthHeaders() },
        body: JSON.stringify({ brand_id: brandId, message }),
      }).then(handleResponse),
  },

  // Memory (Hindsight)
  memory: {
    getOverview: (brandId) =>
      fetch(`${API_BASE}/memory/overview?brand_id=${brandId}`, {
        headers: { ...getAuthHeaders() },
      }).then(handleResponse),

    recall: (brandId, query, limit = 5) =>
      fetch(`${API_BASE}/memory/recall?brand_id=${brandId}&query=${encodeURIComponent(query)}&limit=${limit}`, {
        headers: { ...getAuthHeaders() },
      }).then(handleResponse),
  },

  // Recommendations & Experiments
  experiments: {
    listRecommendations: (brandId) =>
      fetch(`${API_BASE}/recommendations?brand_id=${brandId}`, {
        headers: { ...getAuthHeaders() },
      }).then(handleResponse),

    updateRecommendationStatus: (recId, status) =>
      fetch(`${API_BASE}/recommendations/${recId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json", ...getAuthHeaders() },
        body: JSON.stringify({ status }),
      }).then(handleResponse),

    listExperiments: (brandId) =>
      fetch(`${API_BASE}/experiments?brand_id=${brandId}`, {
        headers: { ...getAuthHeaders() },
      }).then(handleResponse),

    evaluate: (experimentId, actualResults) =>
      fetch(`${API_BASE}/experiments/${experimentId}/evaluate`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...getAuthHeaders() },
        body: JSON.stringify({ actual_results: actualResults }),
      }).then(handleResponse),
  },
};
