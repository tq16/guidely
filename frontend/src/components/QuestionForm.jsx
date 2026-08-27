function QuestionForm({ question, onQuestionChange, onSubmit, isLoading, error }) {
  return (
    <section className="card">
      <form onSubmit={onSubmit}>
        <label htmlFor="question">Your question</label>
        <div className="question-row">
          <input id="question" type="text" value={question} onChange={(event) => onQuestionChange(event.target.value)} placeholder="Example: How many annual leave days do employees receive?" />
          <button type="submit" disabled={isLoading}>{isLoading ? "Finding answer..." : "Ask Guidely"}</button>
        </div>
      </form>
      {error && <p className="error-message">{error}</p>}
    </section>
  );
}

export default QuestionForm;
