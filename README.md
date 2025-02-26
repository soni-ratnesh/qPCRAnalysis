# qPCRAnalysis

## Project Structure

```
project-root/
│
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── file_upload.py   # File upload and processing endpoints
│   │   │   │   └── download.py      # File download endpoint
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── core/
│   │   ├── config.py        # Configuration settings
│   │   └── __init__.py
│   ├── services/
│   │   ├── processing.py     # Data processing logic
│   │   ├── plotting.py       # Plot generation
│   │   └── __init__.py
│   ├── models/
│   │   ├── file_model.py     # Pydantic models
│   │   └── __init__.py
│   ├── utils/
│   │   └── file_handler.py   # File handling utilities
│   ├── main.py               # FastAPI application
│   └── __init__.py
│
├── data/
│   └── uploads/             # Directory to store uploaded files
│
├── output/
│   └── processed/           # Directory to store processed files
│
├── Dockerfile               # Docker configuration
├── requirements.txt         # Python dependencies
└── docker-compose.yml       # Docker Compose for multi-container setup
```