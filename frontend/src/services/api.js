const API_URL = "http://127.0.0.1:8000";

async function request(path, options, fallbackMessage) {
  const response = await fetch(`${API_URL}${path}`, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || fallbackMessage);
  return data;
}

export function askQuestion(question) {
  return request("/search/ask", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question }) }, "Could not get an answer.");
}

export function uploadDocument(file) {
  const formData = new FormData();
  formData.append("file", file);
  return request("/documents/upload", { method: "POST", body: formData }, "Could not upload the document.");
}

export function getUploadedDocuments() {
  return request("/documents/uploaded", undefined, "Could not load uploaded documents.");
}

export function deleteDocument(fileName) {
  return request(`/documents/uploaded/${encodeURIComponent(fileName)}`, { method: "DELETE" }, "Could not delete the document.");
}

export function reindexDocuments() {
  return request("/documents/reindex", { method: "POST" }, "Could not reindex documents.");
}

export function getDocumentContent(fileName) {
  return request(`/documents/uploaded/${encodeURIComponent(fileName)}/content`, undefined, "Could not open the document.");
}

export function updateDocumentContent(fileName, content) {
  return request(`/documents/uploaded/${encodeURIComponent(fileName)}/content`, { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ content }) }, "Could not save the document.");
}
