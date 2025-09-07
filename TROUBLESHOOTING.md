# OpenManus Setup Troubleshooting

## Common Errors and Solutions

### 1. ModuleNotFoundError: No module named 'pydantic'
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Config file missing
**Solution:** Create config file
```bash
cp config/config.example.toml config/config.toml
# Edit config/config.toml and set your API key
```

### 3. API Key not set
**Solution:** Edit config/config.toml and replace YOUR_API_KEY_HERE with your actual API key

### 4. Network timeouts during pip install
**Solution:** Try installing core packages individually:
```bash
pip install pydantic openai loguru fastapi uvicorn
```

### 5. Browser automation not working
**Solution:** Install playwright browsers:
```bash
pip install playwright
playwright install
```

## Quick Setup Check
Run the setup script to diagnose issues:
```bash
python setup_check.py
```
