# Use the Ubuntu base image
FROM ubuntu:latest

# Install necessary packages
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -ms /bin/bash steampipeuser

# Install Steampipe as root
USER root
RUN curl -fsSL https://steampipe.io/install/steampipe.sh | sh

# Switch to the non-root user
USER steampipeuser
RUN steampipe plugin install aws \
    && steampipe plugin install gcp \
    && steampipe plugin install azure

# Set up the virtual environment
RUN python3 -m venv /home/steampipeuser/venv

# Activate the virtual environment and install FastAPI and Uvicorn
RUN /home/steampipeuser/venv/bin/pip install fastapi uvicorn

# Add application code
COPY main.py /home/steampipeuser/main.py
COPY app /home/steampipeuser/app

# Expose the port on which FastAPI will run
EXPOSE 8000

# Set the working directory
WORKDIR /home/steampipeuser

# Set the virtual environment path in the environment variable
ENV PATH="/home/steampipeuser/venv/bin:$PATH"

# Run FastAPI server using the virtual environment
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
