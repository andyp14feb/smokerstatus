FROM python:3.8.20-slim

# Set working directory to root (or use any consistent name like /code)
WORKDIR /flaskapp

# Copy everything into the container
COPY . /flaskapp

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=app:app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=$PORT


EXPOSE 8000

# Use Railway's injected $PORT
CMD ["sh", "-c", "flask run --host=0.0.0.0 --port=$PORT"]
