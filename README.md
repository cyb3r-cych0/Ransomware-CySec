# Ransomware-CySec

### Execution Flow

```mathematica
1. Take Website URL as Input
2. Crawl Entire Website
3. Extract & Display All Links
4. Fetch Page Content
5. Extract Files / Scripts / Downloads
6. Run Ransomware Detection Engine
7. Display Risk Report
```

### Architecture


### Dependencies
#### Install
```css
pip install -r requirements.txt
```

### Run server
```bash
uvicorn app.api:app --reload
```

### Test Browser
```bash
http://127.0.0.1:8000/scan?url=https://example.com
```
