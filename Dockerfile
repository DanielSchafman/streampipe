# Use the Ubuntu base image
FROM ubuntu:latest

# Install necessary packages
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -ms /bin/bash steampipeuser

# Install Steampipe as root
USER root
RUN curl -fsSL https://steampipe.io/install/steampipe.sh | sh

# Switch to the non-root user
USER steampipeuser

# Install all plugins as the non-root user
RUN steampipe plugin install aws \
    && steampipe plugin install gcp \
    && steampipe plugin install azure

# Add your configuration script
COPY configure_streampipe.py /home/steampipeuser/configure_streampipe.py

# Set the working directory
WORKDIR /home/steampipeuser

# Run the configuration script
USER root
RUN python3 configure_streampipe.py

# Keep the container running in the background
CMD ["tail", "-f", "/dev/null"]