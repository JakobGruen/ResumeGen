# Resume Generator Tests

This directory contains comprehensive pytest-based tests for both the CLI script and API modes of Resume Generator.

## 🚀 Quick Start

```bash
# Test everything with automatic Docker management
pytest tests/ --with-docker -v

# Or test just the CLI functionality (no Docker needed)
pytest tests/ -m "script" -v
```

## Test Organization

### 🧪 Test Types

- **Script Tests** (`test_script.py`): Test CLI functionality without external dependencies
- **API Tests** (`test_api.py`): Test microservice API endpoints (requires running services)

### 🏷️ Test Markers

- `@pytest.mark.cli`: CLI functionality tests
- `@pytest.mark.api`: API service tests

## Setup

### Prerequisites

- **Docker Desktop**: Required for API tests
- **Python with uv**: For running tests and managing dependencies

### Installation

```bash
# 1. Install Docker Desktop (if not already installed)
brew install --cask docker

# 2. Start Docker Desktop
open -a Docker

# 3. Install development dependencies
uv pip install -e ".[dev]"

# 4. Verify setup
docker ps                    # Should work without sudo
pytest tests/ -m "script"    # Test script functionality
pytest tests/ --with-docker  # Test everything with automatic Docker
```

## Running Tests

### ✅ Script Tests Only (No External Dependencies)

```bash
# Run only CLI/script tests - works without any services
pytest tests/ -m "script" -v
```

### 🐳 API Tests (Requires Docker Desktop)

**Option 1: Automatic Docker Management** _(Recommended)_

```bash
# Automatically starts/stops Docker services for testing
# Requires Docker Desktop to be running
pytest tests/ -m "api" --with-docker -v
```

**Option 2: Manual Service Management** _(For development/debugging)_

```bash
# 1. Start services manually
docker compose up -d

# 2. Run API tests
pytest tests/ -m "api" -v

# 3. Stop services when done
docker compose down
```

### 📊 All Tests

```bash
# Run everything with automatic Docker management (recommended)
pytest tests/ --with-docker -v

# Run all tests (will skip API tests if services aren't available)
pytest tests/ -v
```

### Selective Testing

```bash
# Run only fast tests (exclude slow integration tests)
pytest tests/ -m "not slow"

# Run only integration tests
pytest tests/ -m "integration"

# Run specific test
pytest tests/test_api.py::TestResumeGeneratorAPI::test_health_check
```

## 🔧 Troubleshooting

### Docker Desktop Setup

```bash
# Install Docker Desktop (if not already installed)
brew install --cask docker

# Start Docker Desktop
open -a Docker

# Verify Docker is working (should work without sudo)
docker ps
docker compose version
```

### API Tests Failing with Connection Errors

```bash
# Error: requests.exceptions.ConnectionError: Connection refused
# Solution 1: Use automatic Docker management (recommended)
pytest tests/ -m "api" --with-docker -v

# Solution 2: Start services manually
docker compose up -d
pytest tests/ -m "api" -v
docker compose down
```

### Docker Permission Issues

```bash
# If you see "permission denied" or need sudo:
# 1. Ensure Docker Desktop is installed (not Docker Engine)
# 2. Check for conflicting DOCKER_HOST environment variable
echo $DOCKER_HOST  # Should be empty for Docker Desktop

# 3. Remove any incorrect DOCKER_HOST exports from shell config
# Edit ~/.zshrc or ~/.bashrc and remove lines like:
# export DOCKER_HOST=unix:///some/path
```

### Script Tests Failing

```bash
# Error: Command 'uv' not found
# Solution: Ensure uv is installed and in PATH
pip install uv

# Error: Module not found
# Solution: Install in development mode
uv pip install -e ".[dev]"
```

## ✅ Success Indicators

When everything is working correctly, you should see:

```bash
# Docker setup is working
$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

# Script tests pass
$ pytest tests/ -m "script" -v
========================= 9 passed, 10 deselected =========================

# API tests with automatic Docker
$ pytest tests/ -m "api" --with-docker -v
🐳 Starting Docker Compose services...
⏳ Waiting for services to be ready...
✅ Services are ready!
========================= 10 passed, 9 deselected =========================
🛑 Stopping Docker Compose services...

# All tests pass
$ pytest tests/ --with-docker -v
========================= 19 passed =========================
```

## 📁 Test Structure

- `conftest.py` - Pytest fixtures, Docker management, and configuration
- `test_api.py` - API microservice tests (marked with @pytest.mark.api)
- `test_script.py` - CLI script tests (marked with @pytest.mark.api)
- `output/` - Generated test files (created automatically, gitignored)

## ✅ Test Coverage

### Script Tests (`test_script.py`)

- ✅ Resume generation with default paths
- ✅ Resume generation with custom output directory
- ✅ Cover letter generation
- ✅ Output format options (html, pdf, both)
- ✅ File existence validation
- ✅ PDF structure validation
- ✅ Command line argument handling
- ✅ Integration with complex data structures

### API Tests (`test_api.py`)

- ✅ Health check endpoint
- ✅ Resume generation (HTML and PDF)
- ✅ Cover letter generation (HTML and PDF)
- ✅ Different output formats (html, pdf, both)
- ✅ Error handling for invalid data
- ✅ Data integrity verification
- ✅ Concurrent request handling
- ✅ PDF structural validation
- ✅ Base64 content encoding/decoding

## 📄 Generated Files

Test runs automatically create output files in `tests/output/`:

- `test_resume.html` - Generated resume HTML
- `test_resume.pdf` - Generated resume PDF
- `test_cover_letter.html` - Generated cover letter HTML
- `test_cover_letter.pdf` - Generated cover letter PDF

These files are:

- ✅ **Automatically validated** for structure and content during tests
- ✅ **Automatically cleaned up** after test completion
- ✅ **Available for manual inspection** to verify output quality
- ✅ **Gitignored** to avoid committing test artifacts

## 🎯 Best Practices

- **Development**: Use `pytest tests/ -m "script"` for quick feedback without Docker
- **Integration Testing**: Use `pytest tests/ --with-docker` for comprehensive testing
- **CI/CD**: Configure with `--with-docker` for automated testing environments
- **Debugging**: Use manual Docker management when you need to inspect running services
