# Google Dorks for AI Research & Security auditing

This guide provides advanced Google search operators ("Dorks") specifically tailored for finding AI resources, datasets, and potential security exposures.

## 🕵️ Research Dorks

### Finding Datasets
*   `site:kaggle.com "dataset" "medical imaging"` - Find specific datasets on Kaggle.
*   `site:gov filetype:csv "climate change"` - Locate CSV datasets on government websites.
*   `site:edu filetype:xls "survey results"` - Find Excel data from educational institutions.
*   `intitle:"index of" "dataset" "json"` - Find open directories containing JSON datasets.

### Finding AI Models & Papers
*   `site:huggingface.co "text-to-image"` - Search for specific model types on Hugging Face.
*   `site:arxiv.org "large language models" "survey"` - Find survey papers on Arxiv.
*   `filetype:pdf "neural network" "tutorial"` - Find PDF tutorials.

## 🛡️ Security Auditing (Ethical Use Only)

### Exposed Configuration Files
*   `filetype:env "OPENAI_API_KEY"` - **Warning:** Search for exposed .env files (do not exploit!).
*   `ext:json "google_application_credentials"` - Find exposed Google Cloud keys.
*   `inurl:/.git/HEAD` - Find exposed .git directories.

### Admin Panels & Dashboards
*   `inurl:admin "login"` - Find admin login pages.
*   `intitle:"dashboard" "status"` - Find status dashboards.

## 🤖 AI-Specific Dorks

*   `inurl:openai "api"` - Find pages discussing OpenAI API usage.
*   `site:github.com "midjourney" "prompt"` - Find Midjourney prompt collections on GitHub.
*   `site:discord.com "stable diffusion"` - Search publicly indexed Discord discussions.

---
**Disclaimer:** These dorks are for educational and research purposes only. Unauthorized access to computer systems is illegal.
