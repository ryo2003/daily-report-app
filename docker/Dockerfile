FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy only the requirements file to leverage Docker cache
COPY docker/requirements.txt /app/requirements.txt

# Install the Linux dependencies and Python packages in one step
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && pip3 install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code last to prevent unnecessary rebuilds
COPY ./myapp /app/
COPY ./docker /docker/

# Expose the port
EXPOSE 8501

# Add a health check for the Streamlit service
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Specify the entry point
#ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
