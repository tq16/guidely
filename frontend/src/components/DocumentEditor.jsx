function DocumentEditor({ fileName, content, message, isLoading, isSaving, onContentChange, onSave, onCancel }) {
  if (!fileName) return null;
  return (
    <section className="editor-card">
      <div className="editor-header">
        <div>
          <p className="section-label">EDIT DOCUMENT</p>
          <h2>{fileName}</h2>
        </div>
        <button className="cancel-button" onClick={onCancel}>Cancel</button>
      </div>
      {isLoading ? (
        <p className="empty-message">Opening document...</p>
      ) : (
        <>
          <textarea className="document-editor" value={content} onChange={(event) => onContentChange(event.target.value)} />
          <div className="editor-footer">
            <button onClick={onSave} disabled={isSaving}>{isSaving ? "Saving..." : "Save and reindex"}</button>
            {message && <p className="upload-message">{message}</p>}
          </div>
        </>
      )}
    </section>
  );
}

export default DocumentEditor;
