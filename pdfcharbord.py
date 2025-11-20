import gradio as gr
from llama_index.readers.file import PDFReader
from llama_index.core import VectorStoreIndex
import os

index = None
query_engine = None

# Load PDF + create index
def load_pdf(file):
    global index, query_engine

    if file is None:
        return "❌ Please upload a PDF."

    # Save uploaded PDF locally
    pdf_path = "uploaded.pdf"
    with open(pdf_path, "wb") as f:
        f.write(file.read())

    # Read PDF
    reader = PDFReader()
    documents = reader.load_data(file=pdf_path)

    # Build index
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

    return "✅ PDF processed successfully! Now ask questions."

# Chat with PDF
def chat_with_pdf(question):
    global query_engine

    if query_engine is None:
        return "⚠️ Please upload and process a PDF first."

    response = query_engine.query(question)
    return str(response)

# UI
with gr.Blocks() as demo:
    gr.Markdown("## 📘 PDF Chatbot — Upload PDF & Ask Anything!")

    pdf_file = gr.File(label="Upload PDF", file_types=[".pdf"])
    upload_btn = gr.Button("Process PDF")
    upload_output = gr.Textbox(label="Status")

    upload_btn.click(load_pdf, inputs=pdf_file, outputs=upload_output)

    question = gr.Textbox(label="Ask a question from the PDF")
    answer = gr.Textbox(label="Answer")

    question.submit(chat_with_pdf, inputs=question, outputs=answer)

demo.launch()
