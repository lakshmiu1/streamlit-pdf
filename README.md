📄 Chat with PDF — LLaMA 2 + LangChain + Streamlit
A local, privacy-friendly chatbot that lets you upload a PDF and have a conversation with its contents — powered by LLaMA 2 running entirely on your machine.

🚀 Features

Upload any PDF and chat with it in natural language
Fully local — no OpenAI API key, no data sent to the cloud
Powered by LLaMA 2 (7B) via llama-cpp-python
Semantic search over PDF content using FAISS + HuggingFace embeddings
Conversational memory — follows the thread of your questions
Clean Streamlit chat UI


🧱 Project Structure
streamlit-pdf/
├── app.py              # Streamlit entry point
├── fileingestor.py     # PDF loading, embedding, vector store, and chat chain
├── loadllm.py          # LLaMA 2 model loader
├── requirements.txt    # Python dependencies
├── vectorstore/        # Auto-generated FAISS index (git-ignored)
└── llama-2-7b-chat.Q4_K_M.gguf  # LLaMA 2 model file (download separately)

⚙️ Setup
1. Clone the repo
bashgit clone https://github.com/lakshmiu/streamlit-pdf.git
cd streamlit-pdf
2. Create and activate a virtual environment
bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies
bashpip install -r requirements.txt
On Mac (Apple Silicon), install llama-cpp-python with Metal support for GPU acceleration:
bashCMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
4. Download the LLaMA 2 model
Download the quantized model file and place it in the project root:

Model: llama-2-7b-chat.Q4_K_M.gguf
Source: TheBloke on HuggingFace

streamlit-pdf/
└── llama-2-7b-chat.Q4_K_M.gguf   ← place it here
5. Run the app
bashstreamlit run app.py

🖥️ Usage

Open the app in your browser (usually http://localhost:8501)
Use the sidebar to upload a PDF file
Wait for the model to load and the PDF to be indexed
Type questions in the chat input and press Send


📦 Dependencies
PackagePurposestreamlitWeb UIstreamlit-chatChat message componentslangchain-classicRetrieval and document chainslangchain-communityPDF loader, FAISS vector storelangchain-huggingfaceHuggingFace embeddingsllama-cpp-pythonRun LLaMA 2 locallysentence-transformersEmbedding model (all-MiniLM-L6-v2)faiss-cpuVector similarity searchpymupdfPDF parsing

🔧 Configuration
Key settings in loadllm.py:
ParameterDefaultDescriptionn_gpu_layers40Layers offloaded to GPU (Metal on Mac)n_ctx4096Context window size in tokensn_batch512Batch size for prompt processing
Increase n_ctx if you see Requested tokens exceed context window errors.

🛠️ Troubleshooting
ModuleNotFoundError: No module named 'langchain.chains'
→ Install langchain-classic: pip install langchain-classic
Requested tokens exceed context window
→ Increase n_ctx in loadllm.py to 8192 or higher
llama-cpp-python install fails on Mac
→ Use: CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python --force-reinstall --no-cache-dir

📝 License
MIT
