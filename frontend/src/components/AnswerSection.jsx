import SourceList from "./SourceList.jsx";

function AnswerSection({ result }) {
  if (!result) return null;
  return (
    <section className="result-section">
      <article className="answer-card">
        <p className="section-label">ANSWER</p>
        <h2>{result.answer}</h2>
        <p className="latency">Answered in {(result.latency_ms / 1000).toFixed(1)} seconds</p>
      </article>
      <SourceList sources={result.sources} />
    </section>
  );
}

export default AnswerSection;
