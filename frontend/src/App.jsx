import { useEffect, useState } from "react";
import AnswerSection from "./components/AnswerSection.jsx";
import DocumentEditor from "./components/DocumentEditor.jsx";
import DocumentLibrary from "./components/DocumentLibrary.jsx";
import QuestionForm from "./components/QuestionForm.jsx";
import UploadSection from "./components/UploadSection.jsx";
import {
  askQuestion as askQuestionRequest,
  deleteDocument as deleteDocumentRequest,
  getDocumentContent,
  getUploadedDocuments,
  reindexDocuments as reindexDocumentsRequest,
  updateDocumentContent,
  uploadDocument as uploadDocumentRequest,
} from "./services/api.js";
import "./App.css";

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

  async function loadUploadedDocuments() {
    try {
      const data = await getUploadedDocuments();
      setUploadedDocuments(data.documents);
    } catch (loadError) {
      setDocumentsError(loadError.message);
    }
  }

  useEffect(() => {
    loadUploadedDocuments();
  }, []);

  async function handleAskQuestion(event) {
    event.preventDefault();
    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }
    setIsLoading(true);
    setError("");
    setResult(null);
    try {
      setResult(await askQuestionRequest(question.trim()));
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  }

  async function handleUploadDocument(event) {
    event.preventDefault();
    if (!selectedFile) {
      setUploadMessage("Please choose a .txt or .pdf document first.");
      return;
    }
    setIsUploading(true);
    setUploadMessage("");
    try {
      const data = await uploadDocumentRequest(selectedFile);
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

  function cancelEditing() {
    setEditingFile("");
    setEditContent("");
    setEditorMessage("");
  }

  async function handleDeleteDocument(fileName) {
    if (!window.confirm(`Delete "${fileName}"? It will no longer be searchable.`)) return;
    setDeletingFile(fileName);
    setDocumentsError("");
    try {
      const data = await deleteDocumentRequest(fileName);
      setUploadMessage(`Deleted and reindexed: ${data.file_name}`);
      if (editingFile === fileName) cancelEditing();
      loadUploadedDocuments();
    } catch (deleteError) {
      setDocumentsError(deleteError.message);
    } finally {
      setDeletingFile("");
    }
  }

  async function handleReindexDocuments() {
    setIsReindexing(true);
    setReindexMessage("");
    setDocumentsError("");
    try {
      const data = await reindexDocumentsRequest();
      setReindexMessage(`Index updated: ${data.document_count} documents and ${data.chunk_count} chunks.`);
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
      const data = await getDocumentContent(fileName);
      setEditContent(data.content);
    } catch (editError) {
      setDocumentsError(editError.message);
      setEditingFile("");
    } finally {
      setIsLoadingEditor(false);
    }
  }

  async function saveEditedDocument() {
    if (!editContent.trim()) {
      setEditorMessage("Document content cannot be empty.");
      return;
    }
    setIsSavingEdit(true);
    setEditorMessage("");
    try {
      const data = await updateDocumentContent(editingFile, editContent);
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
        <p className="subtitle">Ask company-policy questions and get clear answers with sources.</p>
      </section>
      <QuestionForm question={question} onQuestionChange={setQuestion} onSubmit={handleAskQuestion} isLoading={isLoading} error={error} />
      <UploadSection onFileChange={setSelectedFile} onSubmit={handleUploadDocument} isUploading={isUploading} message={uploadMessage} />
      <DocumentLibrary documents={uploadedDocuments} error={documentsError} reindexMessage={reindexMessage} isReindexing={isReindexing} deletingFile={deletingFile} onReindex={handleReindexDocuments} onEdit={startEditing} onDelete={handleDeleteDocument}>
        <DocumentEditor fileName={editingFile} content={editContent} message={editorMessage} isLoading={isLoadingEditor} isSaving={isSavingEdit} onContentChange={setEditContent} onSave={saveEditedDocument} onCancel={cancelEditing} />
      </DocumentLibrary>
      <AnswerSection result={result} />
    </main>
  );
}

export default App;
