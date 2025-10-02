# Assignment-Task

High-Performance API Gateway
============================

This project is a high-performance API Gateway built with FastAPI.
It supports authentication, rate limiting, caching, centralized logging,
and can handle 50k+ requests under load.

Features
--------

- Authentication: JWT-based token verification
- Rate Limiting: Prevent abuse using token bucket algorithm
- Caching: Frequently accessed responses cached in Redis
- Centralized Logging: Structured JSON logs using python-json-logger
- Automated Tests: Using pytest and pytest-asyncio
- Dockerized Deployment: Easy deployment using Docker

Folder Structure
----------------

project_root/
├─ app/
│  ├─ __init__.py          # marks app as a Python package
│  ├─ main.py              # FastAPI app entry point
│  ├─ auth.py              # JWT authentication
│  ├─ cache.py             # Redis caching utilities
│  ├─ rate_limiter.py      # Rate limiting
│  └─ logger.py            # Centralized logging
├─ tests/
│  └─ test_endpoints.py    # Automated tests
├─ requirements.txt
├─ Dockerfile
└─ README.txt

Installation
------------

1. Clone the repository:
   git clone <your-repo-url>
   cd Task_Assignment

2. Create a virtual environment (optional but recommended):
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows

3. Install all dependencies:
   pip install -r requirements.txt

Running the API
---------------

Start the server using Uvicorn:
   uvicorn app.main:app --reload

Open in your browser:
   http://127.0.0.1:8000/docs
This will show the interactive Swagger UI for testing endpoints.

Running Tests
-------------

Run all tests:
   pytest

- Tests are located in the tests/ folder.
- Includes async endpoint tests for authentication, rate limiting, and caching.

Docker Deployment
-----------------

1. Build Docker image:
   docker build -t api-gateway .

2. Run container:
   docker run -p 8000:8000 api-gateway

Notes
-----

- Redis must be running locally for caching (redis://localhost).
- Modify config or environment variables for JWT secret, rate limits, and cache TTL.

Author
------

Shaik Babu
Email: babushaik7701@gmail.com
