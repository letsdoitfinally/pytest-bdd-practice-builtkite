FROM python:3.11-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Default command to run tests
CMD ["pytest", "tests/", "--gherkin-terminal-reporter", "-v"]