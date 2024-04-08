FROM python:3.10

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the application
COPY . .

# Run command to start Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]