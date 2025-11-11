FROM python:3.12

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

ENV PYTHONUNBUFFERED=1
ENV OLLAMA_HOST=http://128.2.220.232:11434/

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]