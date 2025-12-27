# RinkLess Link Checker API

A FastAPI backend service that checks URLs against whitelist and blacklist patterns. Designed for mobile app integration and Railway deployment.

## Features

- Check URLs against configurable whitelist/blacklist
- Domain pattern matching with wildcard support
- Automatic subdomain matching

## Pattern Matching

| Pattern | Matches | Does NOT Match |
|---------|---------|----------------|
| `google.com` | `google.com`, `mail.google.com`, `google.com/search` | `xgoogle.com` |
| `*.google.com` | `mail.google.com`, `www.google.com` | `google.com` |

## Local Development

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Usage

### Check Link

**POST** `/check-link`

```bash
curl -X POST http://localhost:8000/check-link \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com/search"}'
```

**Response:**
```json
{
  "url": "https://google.com/search",
  "status": "safe"
}
```

Status values:
- `safe` - URL matches a whitelist pattern
- `unsafe` - URL matches a blacklist pattern
- `normal` - URL matches neither

### Health Check

**GET** `/health`

```bash
curl http://localhost:8000/health
```

## Configuration

Edit `whitelist.txt` and `blacklist.txt` to add domain patterns:

```
# Comments start with #
google.com          # Matches google.com and *.google.com
*.github.com        # Matches only subdomains
```

## Railway Deployment

1. Push this repository to GitHub
2. Create a new project on [Railway](https://railway.app)
3. Connect your GitHub repository
4. Railway will auto-detect the Python app and deploy

The `Procfile` configures Railway to run the app with uvicorn.
