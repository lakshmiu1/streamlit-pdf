# 📄 Chat with PDF — LLaMA 2 + LangChain + Streamlit

A local, privacy-friendly chatbot that lets you upload a PDF and have a conversation with its contents — powered by LLaMA 2 running entirely on your machine.

---

## 🚀 Features

- 📁 Upload any PDF and chat with it in natural language
- 🔒 Fully local — no OpenAI API key, no data sent to the cloud
- 🦙 Powered by LLaMA 2 (7B) via `llama-cpp-python`
- 🔍 Semantic search over PDF content using FAISS + HuggingFace embeddings
- 💬 Conversational memory — follows the thread of your questions
- 🖥️ Clean Streamlit chat UI

---

## 🧱 Project Structure

```
streamlit-pdf/
├── app.py              # Streamlit entry point
├── fileingestor.py     # PDF loading, embedding, vector store, and chat chain
├── loadllm.py          # LLaMA 2 model loader
├── requirements.txt    # Python dependencies
├── vectorstore/        # Auto-generated FAISS index (git-ignored)
└── llama-2-7b-chat.Q4_K_M.gguf  # LLaMA 2 model file (download separately)
```

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/lakshmiu1/streamlit-pdf.git
cd streamlit-pdf
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Mac (Apple Silicon):** Install `llama-cpp-python` with Metal GPU support:
> ```bash
> CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
> ```

### 4. Download the LLaMA 2 model

Download the quantized model and place it in the project root:

- **Model:** `llama-2-7b-chat.Q4_K_M.gguf`
- **Source:** [TheBloke on HuggingFace](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF)

```
streamlit-pdf/
└── llama-2-7b-chat.Q4_K_M.gguf   ← place it here
```

### 5. Run the app

```bash
streamlit run app.py
```

---

## 🖥️ Usage

1. Open the app in your browser at `http://localhost:8501`
2. Use the **sidebar** to upload a PDF file
3. Wait for the model to load and the PDF to be indexed
4. Type your questions in the chat input and press **Send**

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI |
| `streamlit-chat` | Chat message components |
| `langchain-classic` | Retrieval and document chains |
| `langchain-community` | PDF loader, FAISS vector store |
| `langchain-huggingface` | HuggingFace embeddings |
| `llama-cpp-python` | Run LLaMA 2 locally |
| `sentence-transformers` | Embedding model (`all-MiniLM-L6-v2`) |
| `faiss-cpu` | Vector similarity search |
| `pymupdf` | PDF parsing |

---

## 🔧 Configuration

Key settings in `loadllm.py`:

| Parameter | Default | Description |
|---|---|---|
| `n_gpu_layers` | `40` | Layers offloaded to GPU (Metal on Mac) |
| `n_ctx` | `4096` | Context window size in tokens |
| `n_batch` | `512` | Batch size for prompt processing |

> Increase `n_ctx` to `8192` or higher if you see **"Requested tokens exceed context window"** errors.

---

## 🛠️ Troubleshooting

**`ModuleNotFoundError: No module named 'langchain.chains'`**
```bash
pip install langchain-classic
```

**`Requested tokens exceed context window`**
- Increase `n_ctx` in `loadllm.py` to `8192` or higher

**`llama-cpp-python` install fails on Mac**
```bash
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
```

---

## 📝 License

MIT
