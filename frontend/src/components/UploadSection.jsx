function UploadSection({ onFileChange, onSubmit, isUploading, message }) {
  return (
    <section className="upload-card">
      <div>
        <p className="section-label">ADD KNOWLEDGE</p>
        <h2>Upload a company document</h2>
        <p>Upload a TXT or PDF file. Guidely indexes it automatically.</p>
      </div>
      <form className="upload-form" onSubmit={onSubmit}>
        <input type="file" accept=".txt,.pdf" onChange={(event) => onFileChange(event.target.files[0] || null)} />
        <button type="submit" disabled={isUploading}>{isUploading ? "Uploading..." : "Upload document"}</button>
      </form>
      {message && <p className="upload-message">{message}</p>}
    </section>
  );
}

export default UploadSection;
