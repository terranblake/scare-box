# Scare Box Backend

FastAPI-based backend for the Scare Box Halloween trick-or-treat system.

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Development Dependencies (Optional)

```bash
pip install -r requirements-dev.txt
```

## Validation

Run validation script to test components without hardware:

```bash
python validate.py
```

## Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=backend --cov-report=html
```

## Running the Server

### Development Mode (with auto-reload)

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## WebSocket Connection

Connect to: `ws://localhost:8000/ws`

## Configuration

Edit `config.yaml` to customize:

- Operating mode (child/adult)
- Audio trigger settings
- Timing parameters
- Hardware device names
- Server settings

## Project Structure

```
backend/
├── api/                 # REST API endpoints
├── hardware/            # Hardware controllers
├── websocket/           # WebSocket infrastructure
├── utils/               # Utilities (event logging)
├── tests/               # Unit tests
├── config.py            # Configuration management
├── state_machine.py     # State machine
├── controller.py        # Main orchestration controller
├── main.py              # FastAPI application
└── validate.py          # Validation script
```

## Development

### Code Quality

Format code:

```bash
black .
```

Check linting:

```bash
flake8
```

Type checking:

```bash
mypy .
```

### Adding New Features

1. Write tests first in `tests/`
2. Implement feature
3. Run tests: `pytest`
4. Validate: `python validate.py`
5. Commit with semantic versioning

## Troubleshooting

### Hardware Not Found

If hardware devices are not detected:

1. Check device connections (USB-C, WiFi, Bluetooth)
2. Update device names in `config.yaml`
3. Run in simulation mode (hardware controllers handle missing devices gracefully)

### Import Errors

Ensure you're in the virtual environment:

```bash
source venv/bin/activate
```

### Port Already in Use

Change the port in `config.yaml` or use:

```bash
uvicorn main:app --port 8001
```
