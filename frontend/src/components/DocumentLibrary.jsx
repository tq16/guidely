function DocumentLibrary({ documents, error, reindexMessage, isReindexing, deletingFile, onReindex, onEdit, onDelete, children }) {
  return (
    <section className="documents-section">
      <div className="documents-title">
        <div>
          <p className="section-label">KNOWLEDGE LIBRARY</p>
          <h2>Uploaded documents</h2>
        </div>
        <div className="documents-actions">
          <span className="document-count">{documents.length} file{documents.length === 1 ? "" : "s"}</span>
          <button className="reindex-button" onClick={onReindex} disabled={isReindexing}>{isReindexing ? "Reindexing..." : "Reindex all"}</button>
        </div>
      </div>
      {error && <p className="error-message">{error}</p>}
      {reindexMessage && <p className="upload-message">{reindexMessage}</p>}
      {documents.length === 0 ? (
        <p className="empty-message">No uploaded documents yet.</p>
      ) : (
        <div className="documents-list">
          {documents.map((document) => (
            <article className="document-row" key={document.file_name}>
              <div>
                <strong>{document.file_name}</strong>
                <p>{document.file_type} · {document.size_kb} KB</p>
              </div>
              <div className="document-buttons">
                {document.file_type === "TXT" && <button className="edit-button" onClick={() => onEdit(document.file_name)}>Edit</button>}
                <button className="delete-button" onClick={() => onDelete(document.file_name)} disabled={deletingFile === document.file_name}>
                  {deletingFile === document.file_name ? "Deleting..." : "Delete"}
                </button>
              </div>
            </article>
          ))}
        </div>
      )}
      {children}
    </section>
  );
}

export default DocumentLibrary;
