FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Default command
ENTRYPOINT ["python", "inference.py"]
CMD ["--task", "easy", "--episodes", "5"]
