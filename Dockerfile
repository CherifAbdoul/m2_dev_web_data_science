# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose Flask's default port
EXPOSE 5000

# Expose Streamlit's default port
EXPOSE 8501

# Start both Flask and Streamlit applications
CMD ["bash", "-c", "flask run --host=0.0.0.0 & streamlit run app.py --server.port=8501 --server.enableCORS false"]
