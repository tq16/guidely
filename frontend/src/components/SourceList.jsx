function SourceList({ sources }) {
  return (
    <section className="sources-section">
      <p className="section-label">SOURCES USED</p>
      <div className="sources-list">
        {sources.map((source, index) => (
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
  );
}

export default SourceList;
