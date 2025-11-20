# 🤖 BDM Copilot

**AI-Powered Sales Assistant for Dell Infrastructure Solutions**

Transform discovery notes into professional proposals, BOMs, and ready-to-send emails — all running **100% locally** for complete data privacy.

---

## 🎯 What It Does

BDM Copilot converts raw customer discovery notes into comprehensive sales deliverables:

- **📊 Market Analysis** — AI-generated insights aligned with Adrian's 3-pillar BDM methodology
- **💼 Solution Options** — 3 tailored Dell infrastructure recommendations (Good/Better/Best)
- **📝 Bill of Materials** — Detailed BOM with SKUs, specs, and pricing estimates (CSV export)
- **📧 Professional Emails** — Customer recaps, partner requests, and executive summaries
- **⬇️ Export Options** — Outlook-ready .eml files and Salesforce JSON payloads

### ✨ Key Features

✅ **Completely Offline** — No cloud APIs, no data leaves your machine  
✅ **Dell Knowledge Base** — Powered by real Dell documentation (VxRail, PowerStore, ProSupport)  
✅ **Adrian's Methodology** — Built-in 3-pillar BDM framework (Market Trends, Product Portfolio, Competitive Differentiation)  
✅ **Intelligent Fallbacks** — Works even if AI model is unavailable  
✅ **Export Ready** — Download emails as .eml or Salesforce JSON with one click

---

## 🤖 AI Technology Stack

### Local Language Model

- **Model:** Meta Llama 3.2 (3B parameters)
- **Quantization:** Q4_K_M (4-bit optimized)
- **Size:** ~2GB on disk
- **Runtime:** Ollama (local inference server)
- **Performance:** Real-time generation on consumer hardware
- **Privacy:** 100% local processing, zero external API calls

### Knowledge Base Architecture

- **Embeddings:** Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Database:** ChromaDB (persistent local storage)
- **Document Processing:** PyPDF + custom chunking
- **Retrieval:** Semantic search with top-K ranking
- **Source Material:** Official Dell product documentation (5 PDFs)

### Framework

- **UI:** Streamlit (Python web framework)
- **RAG Pipeline:** LangChain components
- **Pattern:** Retrieval-Augmented Generation with fallback templates

---

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.9+
python3 --version

# Ollama (for local AI model)
brew install ollama
```

### Installation

```bash
# Clone repository
git clone https://github.com/abbasbukhari/BDM-Copilot.git
cd BDM-Copilot

# Install dependencies
pip install -r requirements.txt

# Pull AI model
ollama pull llama3.2:3b

# Start Ollama service
ollama serve
```

### Run the App

```bash
# Start Streamlit app
streamlit run app/main.py

# Open browser to http://localhost:8502
```

---

## 📖 How to Use

### 1️⃣ Input Discovery Notes

Paste raw notes from customer meetings:

```
Customer: Acme Health
Industry: Healthcare
Pain: Running out of storage (60TB), backup windows too long
Budget: $800K, Timeline: Q2 2026
Requirements: HIPAA compliance, 99.9% uptime, RPO < 1 hour
```

### 2️⃣ Review AI Analysis

Get instant analysis following Adrian's 3 pillars:

- **Market Trends** — Why this solution matters now
- **Product Portfolio** — Specific Dell recommendations (VxRail, PowerStore, ProSupport)
- **Competitive Advantage** — Dell vs. HPE/Nutanix/Cisco

### 3️⃣ Generate Outputs

- **3 Solution Options** — Tailored configurations with tradeoffs
- **Detailed BOM** — Hardware specs, licensing, services (downloadable CSV)

### 4️⃣ Export Communications

Download ready-to-send emails:

- **Customer Recap** — Thank you + next steps
- **Partner Request** — Pricing/lead time check
- **Executive Summary** — Business case for C-level

**Export Formats:**

- `.eml` files → Open directly in Outlook/Apple Mail
- Salesforce JSON → Import into CRM

---

## 🏗️ Architecture

```
┌─────────────────────┐
│  Discovery Notes    │
│   (User Input)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────┐
│     Knowledge Base Engine           │
│  ┌─────────────┐  ┌──────────────┐ │
│  │ Vector DB   │  │ Dell PDFs    │ │
│  │ (ChromaDB)  │  │ (5 docs)     │ │
│  └─────────────┘  └──────────────┘ │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│    Local AI Model (Llama 3.2 3B)   │
│    + Adrian's BDM Prompt Template   │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│        Structured Output            │
│  • Market Analysis                  │
│  • Solution Architecture            │
│  • Competitive Advantage            │
│  • Business Impact                  │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│      Deliverable Generation         │
│  • Solution Options (3)             │
│  • BOM (CSV)                        │
│  • Emails (.eml + Salesforce JSON)  │
└─────────────────────────────────────┘
```

---

## 📁 Project Structure

```
BDM-Copilot/
├── app/
│   └── main.py                 # Streamlit UI (Input/Analysis/Outputs/Communications)
├── engine/
│   ├── knowledge_base.py       # RAG orchestration & document retrieval
│   ├── llm_engine.py           # Local AI model integration
│   ├── pdf_processor.py        # Document ingestion & chunking
│   └── vector_db.py            # ChromaDB vector search
├── data/
│   ├── pdfs/                   # Dell documentation (5 PDFs)
│   ├── processed/              # Cache & preprocessed chunks
│   └── vectordb/               # ChromaDB persistence
├── templates/
│   ├── adrian_bdm_prompt_template.md  # System prompt template
│   ├── bom_template.csv.md            # BOM structure reference
│   └── *_email_template.md            # Email fallback templates
├── tests/
│   ├── test_llm_integration.py        # AI model validation
│   └── quick_check.py                 # Environment health check
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🔒 Privacy & Security

- **No Cloud APIs** — All processing happens on your local machine
- **No Data Transmission** — Discovery notes never leave your computer
- **Offline-First** — Works without internet connection (after initial setup)
- **Local Storage** — Vector database and cache stored locally
- **GDPR/Compliance Ready** — No third-party data processing

---

## 🎓 Adrian's 3-Pillar BDM Methodology

Every AI-generated output follows Adrian's proven framework:

### 1. 📈 Market Trends & Use Cases

- Identify IT market trends driving customer needs
- Connect customer scenario to industry patterns
- Explain WHY this solution matters now

### 2. 🧰 Product Portfolio & Services Mapping

- Recommend specific Dell products (VxRail, PowerStore, PowerEdge)
- Include Dell services (ProSupport, ProDeploy, APEX)
- Show complete solution architecture

### 3. ⚔️ Competitive Differentiation

- Compare Dell vs. HPE/Nutanix/Cisco
- Highlight unique Dell advantages
- Provide concrete business benefits (TCO, support, deployment speed)

---

## 📊 System Requirements

### Minimum

- **CPU:** 4 cores (Intel/AMD/Apple Silicon)
- **RAM:** 8GB
- **Storage:** 5GB free space
- **OS:** macOS, Linux, or Windows (with WSL)

### Recommended

- **CPU:** 8+ cores
- **RAM:** 16GB
- **Storage:** 10GB SSD
- **GPU:** Optional (speeds up inference)

---

## 🛠️ Technology Dependencies

```
Python 3.9+
├── streamlit          # Web UI framework
├── pandas             # BOM table generation
├── sentence-transformers  # Local embeddings
├── chromadb           # Vector database
├── pypdf              # PDF processing
├── langchain          # RAG components
└── requests           # Ollama API client

Ollama
└── llama3.2:3b       # 3B parameter language model
```

---

## 🧪 Testing & Validation

```bash
# Quick environment check
python3 quick_check.py

# LLM integration test
python3 test_llm_integration.py

# Full app status check
python3 test_app_status.py
```

Expected output:

```
✅ PDF Files: 5 documents
✅ Cache File: 110.5 KB
✅ Vector DB: Found
✅ LLM Connection: OK
✅ All tests passed
```

---

## 📈 Roadmap

**Current (v0.1):**

- ✅ Local LLM integration
- ✅ Dell knowledge base (5 PDFs)
- ✅ Adrian's 3-pillar methodology
- ✅ Export to .eml and Salesforce JSON

**Next (v0.2):**

- [ ] Expand Dell documentation (PowerEdge, Networking, Storage)
- [ ] Multi-customer session management
- [ ] BOM pricing API integration (optional)
- [ ] Advanced export formats (Word proposals, PowerPoint decks)
- [ ] Chat interface for iterative refinement

**Future:**

- [ ] Model upgrades (Llama 3.1 8B, Mistral 7B)
- [ ] Multi-language support
- [ ] Reference architecture templates
- [ ] Competitive battle cards integration

---

## 🤝 Contributing

This is an internal Dell BDM tool. For feature requests or issues, contact the development team.

---

## 📝 License

Internal Dell Technologies tool. All rights reserved.

---

## 👥 Credits

**Developed for Dell BDM Team**  
**Inspired by Adrian's BDM Methodology**  
**Powered by Open Source AI (Meta Llama 3.2)**

---

## 📧 Support

For questions or demo requests, contact:  
**Abbas Bukhari** — [GitHub](https://github.com/abbasbukhari)

---

**Last Updated:** November 19, 2025  
**Version:** 0.1.0  
**Status:** ✅ Production Ready
