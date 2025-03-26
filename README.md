# Kortex

Kortex is a prompt evaluation system for Large Language Models (LLMs), designed to create, manage, and evaluate prompt workflows.

## Overview

Kortex provides a systematic approach to:
- Create and manage prompt workflows
- Test and evaluate LLM responses
- Track prompt performance metrics
- Optimize prompt engineering processes

## Project Structure

```
kortex/
├── README.md
├── docs/
│   └── kortex_design.md
├── src/
│   ├── api/          # FastAPI application
│   ├── core/         # Core business logic
│   ├── database/     # Database models and migrations
│   └── utils/        # Utility functions
├── tests/            # Test suite
├── config/           # Configuration files
└── requirements.txt  # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nonbios-1/kortex.git
   cd kortex
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the database:
   ```bash
   # Create MySQL database
   mysql -u your_user -p -e "CREATE DATABASE IF NOT EXISTS kortex;"
   
   # Set environment variables
   export DATABASE_URL="mysql+pymysql://your_user:your_password@localhost/kortex"
   ```

4. Initialize the database:
   ```bash
   PYTHONPATH=. python3 src/init_db.py
   ```

5. Start the API server:
   ```bash
   PYTHONPATH=. uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### API Endpoints

- `GET /health`: Health check endpoint
- `POST /workflows/`: Create a new workflow
- `GET /workflows/`: List all workflows
- `GET /workflows/{workflow_id}`: Get a specific workflow
- `PUT /workflows/{workflow_id}`: Update a workflow
- `DELETE /workflows/{workflow_id}`: Delete a workflow

### Example Usage

Create a new workflow:
```bash
curl -X POST http://localhost:8000/workflows/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Workflow", "description": "A test workflow", "prompt_template": "This is a {{test}} template", "parameters": {"test": "sample"}}'
```


Documentation and setup instructions coming soon.

## License

MIT License
