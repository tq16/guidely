import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");
  const [isUploading, setIsUploading] = useState(false);

  const [uploadedDocuments, setUploadedDocuments] = useState([]);
  const [documentsError, setDocumentsError] = useState("");
  const [deletingFile, setDeletingFile] = useState("");

  const [isReindexing, setIsReindexing] = useState(false);
  const [reindexMessage, setReindexMessage] = useState("");

  const [editingFile, setEditingFile] = useState("");
  const [editContent, setEditContent] = useState("");
  const [editorMessage, setEditorMessage] = useState("");
  const [isLoadingEditor, setIsLoadingEditor] = useState(false);
  const [isSavingEdit, setIsSavingEdit] = useState(false);

  useEffect(() => {
    loadUploadedDocuments();
  }, []);

  async function loadUploadedDocuments() {
    try {
      const response = await fetch(`${API_URL}/documents/uploaded`);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Could not load uploaded documents.");
      }

      setUploadedDocuments(data.documents);
    } catch (loadError) {
      setDocumentsError(loadError.message);
    }
  }

  async function askQuestion(event) {
    event.preventDefault();

    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    setIsLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/search/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question.trim(),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Could not get an answer.");
      }

      setResult(data);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  }

  async function uploadDocument(event) {
    event.preventDefault();

    if (!selectedFile) {
      setUploadMessage("Please choose a .txt or .pdf document first.");
      return;
    }

    setIsUploading(true);
    setUploadMessage("");

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch(`${API_URL}/documents/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Could not upload the document.");
      }

      setUploadMessage(`Uploaded and indexed: ${data.file_name}`);
      setSelectedFile(null);
      event.target.reset();
      loadUploadedDocuments();
    } catch (uploadError) {
      setUploadMessage(uploadError.message);
    } finally {
      setIsUploading(false);
    }
  }

  async function deleteDocument(fileName) {
    const shouldDelete = window.confirm(
      `Delete "${fileName}"? It will no longer be searchable.`
    );

    if (!shouldDelete) {
      return;
    }

    setDeletingFile(fileName);
    setDocumentsError("");

    try {
      const response = await fetch(
        `${API_URL}/documents/uploaded/${encodeURIComponent(fileName)}`,
        {
          method: "DELETE",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Could not delete the document.");
      }

      setUploadMessage(`Deleted and reindexed: ${data.file_name}`);

      if (editingFile === fileName) {
        cancelEditing();
      }

      loadUploadedDocuments();
    } catch (deleteError) {
      setDocumentsError(deleteError.message);
    } finally {
      setDeletingFile("");
    }
  }

  async function reindexDocuments() {
    setIsReindexing(true);
    setReindexMessage("");
    setDocumentsError("");

    try {
      const response = await fetch(`${API_URL}/documents/reindex`, {
        method: "POST",
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Could not reindex documents.");
      }

      setReindexMessage(
        `Index updated: ${data.document_count} documents and ${data.chunk_count} chunks.`
      );
    } catch (reindexError) {
      setDocumentsError(reindexError.message);
    } finally {
      setIsReindexing(false);
    }
  }

  async function startEditing(fileName) {
    setEditingFile(fileName);
    setEditContent("");
    setEditorMessage("");
    setDocumentsError("");
    setIsLoadingEditor(true);

    try {
      const response = await fetch(
        `${API_URL}/documents/uploaded/${encodeURIComponent(fileName)}/content`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Could not open the document.");
      }

      setEditContent(data.content);
    } catch (editError) {
      setDocumentsError(editError.message);
      setEditingFile("");
    } finally {
      setIsLoadingEditor(false);
    }
  }

  function cancelEditing() {
    setEditingFile("");
    setEditContent("");
    setEditorMessage("");
  }

  async function saveEditedDocument() {
    if (!editContent.trim()) {
      setEditorMessage("Document content cannot be empty.");
      return;
    }

    setIsSavingEdit(true);
    setEditorMessage("");

    try {
      const response = await fetch(
        `${API_URL}/documents/uploaded/${encodeURIComponent(editingFile)}/content`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            content: editContent,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Could not save the document.");
      }

      setEditorMessage(`Saved and indexed: ${data.file_name}`);
      loadUploadedDocuments();
    } catch (saveError) {
      setEditorMessage(saveError.message);
    } finally {
      setIsSavingEdit(false);
    }
  }

  return (
    <main className="app">
      <section className="hero">
        <p className="label">INTERNAL KNOWLEDGE ASSISTANT</p>
        <h1>Guidely</h1>
        <p className="subtitle">
          Ask company-policy questions and get clear answers with sources.
        </p>
      </section>

      <section className="card">
        <form onSubmit={askQuestion}>
          <label htmlFor="question">Your question</label>

          <div className="question-row">
            <input
              id="question"
              type="text"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Example: How many annual leave days do employees receive?"
            />

            <button type="submit" disabled={isLoading}>
              {isLoading ? "Finding answer..." : "Ask Guidely"}
            </button>
          </div>
        </form>

        {error && <p className="error-message">{error}</p>}
      </section>

      <section className="upload-card">
        <div>
          <p className="section-label">ADD KNOWLEDGE</p>
          <h2>Upload a company document</h2>
          <p>Upload a TXT or PDF file. Guidely indexes it automatically.</p>
        </div>

        <form className="upload-form" onSubmit={uploadDocument}>
          <input
            type="file"
            accept=".txt,.pdf"
            onChange={(event) => setSelectedFile(event.target.files[0] || null)}
          />

          <button type="submit" disabled={isUploading}>
            {isUploading ? "Uploading..." : "Upload document"}
          </button>
        </form>

        {uploadMessage && <p className="upload-message">{uploadMessage}</p>}
      </section>

      <section className="documents-section">
        <div className="documents-title">
          <div>
            <p className="section-label">KNOWLEDGE LIBRARY</p>
            <h2>Uploaded documents</h2>
          </div>

          <div className="documents-actions">
            <span className="document-count">
              {uploadedDocuments.length} file
              {uploadedDocuments.length === 1 ? "" : "s"}
            </span>

            <button
              className="reindex-button"
              onClick={reindexDocuments}
              disabled={isReindexing}
            >
              {isReindexing ? "Reindexing..." : "Reindex all"}
            </button>
          </div>
        </div>

        {documentsError && <p className="error-message">{documentsError}</p>}
        {reindexMessage && <p className="upload-message">{reindexMessage}</p>}

        {uploadedDocuments.length === 0 ? (
          <p className="empty-message">No uploaded documents yet.</p>
        ) : (
          <div className="documents-list">
            {uploadedDocuments.map((document) => (
              <article className="document-row" key={document.file_name}>
                <div>
                  <strong>{document.file_name}</strong>
                  <p>
                    {document.file_type} · {document.size_kb} KB
                  </p>
                </div>

                <div className="document-buttons">
                  {document.file_type === "TXT" && (
                    <button
                      className="edit-button"
                      onClick={() => startEditing(document.file_name)}
                    >
                      Edit
                    </button>
                  )}

                  <button
                    className="delete-button"
                    onClick={() => deleteDocument(document.file_name)}
                    disabled={deletingFile === document.file_name}
                  >
                    {deletingFile === document.file_name ? "Deleting..." : "Delete"}
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}

        {editingFile && (
          <section className="editor-card">
            <div className="editor-header">
              <div>
                <p className="section-label">EDIT DOCUMENT</p>
                <h2>{editingFile}</h2>
              </div>

              <button className="cancel-button" onClick={cancelEditing}>
                Cancel
              </button>
            </div>

            {isLoadingEditor ? (
              <p className="empty-message">Opening document...</p>
            ) : (
              <>
                <textarea
                  className="document-editor"
                  value={editContent}
                  onChange={(event) => setEditContent(event.target.value)}
                />

                <div className="editor-footer">
                  <button
                    onClick={saveEditedDocument}
                    disabled={isSavingEdit}
                  >
                    {isSavingEdit ? "Saving..." : "Save and reindex"}
                  </button>

                  {editorMessage && (
                    <p className="upload-message">{editorMessage}</p>
                  )}
                </div>
              </>
            )}
          </section>
        )}
      </section>

      {result && (
        <section className="result-section">
          <article className="answer-card">
            <p className="section-label">ANSWER</p>
            <h2>{result.answer}</h2>

            <p className="latency">
              Answered in {(result.latency_ms / 1000).toFixed(1)} seconds
            </p>
          </article>

          <section className="sources-section">
            <p className="section-label">SOURCES USED</p>

            <div className="sources-list">
              {result.sources.map((source, index) => (
                <article className="source-card" key={`${source.file_name}-${index}`}>
                  <div className="source-header">
                    <strong>[{index + 1}] {source.file_name}</strong>
                    <span>{Math.round(source.similarity_score * 100)}% match</span>
                  </div>

                  <p>{source.snippet}</p>
                </article>
              ))}
            </div>
          </section>
        </section>
      )}
    </main>
  );
}

export default App;