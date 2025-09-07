# OpenManus Quick Start Guide

## 🚀 Getting Started in 3 Steps

### 1. Install Dependencies
```bash
# Option A: Full installation
pip install -r requirements.txt

# Option B: Minimal installation (if having network issues)
python install_minimal.py
```

### 2. Configure API Keys
```bash
# Edit the config file
nano config/config.toml

# Set your API key (replace YOUR_API_KEY_HERE)
api_key = "sk-your-actual-openai-api-key"
```

### 3. Run OpenManus
```bash
python main.py
```

## 🔧 Troubleshooting

### Common Issues:

1. **ModuleNotFoundError: No module named 'pydantic'**
   ```bash
   pip install pydantic loguru openai
   ```

2. **Config file missing**
   ```bash
   python fix_errors.py
   ```

3. **API key not working**
   - Check your OpenAI account balance
   - Verify API key is correct
   - Make sure you have API access

### Diagnostic Tools:
- `python setup_check.py` - Check your setup
- `python fix_errors.py` - Auto-fix common issues
- `python install_minimal.py` - Install core dependencies

## 📖 Need Help?
Check the full README.md or TROUBLESHOOTING.md for detailed instructions.
