# System Integration: Antigravity Toolkit

This document serves as the integration hub for the "Antigravity" open-source tools into your daily workflow.

## 📂 Toolkit Structure
Location: `~/.gemini/antigravity/scratch/antigravity_toolkit/`

*   `google_dorks.md`: **Intelligence Module.** Cheat sheet for high-level research.
*   `open_source_models.md`: **Generative Engine.** Guide for running Hunyuan 3D locally.
*   `scripts/firecrawl_agent.py`: **Data Ingestion.** Python script to turn unlimited web content into AI-ready markdown.

## 🔗 Workflow Integrations

### 1. Research & Data Mining (The "Dork" Protocol)
**Goal:** Find datasets or vulnerable configs.
**Action:**
1.  Open `google_dorks.md`.
2.  Copy a relevant dork (e.g., `filetype:csv "climate data"`).
3.  Paste into Google Search.
4.  Feed results into **Firecrawl Agent** to extract valid data.

### 2. Automated Web Scraping
**Goal:** Feed fresh web data to your LLMs.
**Setup:**
1.  Get a free API key from [Firecrawl.dev](https://firecrawl.dev).
2.  Export it: `export FIRECRAWL_API_KEY="your_key"`.
3.  Run the agent: `python3 scripts/firecrawl_agent.py`.
**Result:** Clean `scraped_content.md` ready for analysis.

### 3. 3D Asset Pipeline (Zero Cost)
**Goal:** Unlimited 3D props for games/rendering.
**Setup:**
1.  Follow `open_source_models.md` to install Hunyuan 3D.
2.  Run purely local generation (No cloud costs).
3.  Import `.obj` files directly into Blender/Unity.

## 🤖 Future Agent Capabilities
To make these tools native to *Antigravity* (me), ensure these scripts are maintained in this toolkit. I can reference them to write code or execute commands on your behalf.
