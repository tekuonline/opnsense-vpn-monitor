# Use Python 3.9 Alpine for a lightweight image for OPNsense VPN Monitor
FROM python:3.9-alpine

# Add metadata labels
LABEL org.opencontainers.image.title="OPNsense VPN Monitor" \
      org.opencontainers.image.description="Docker-based service that monitors OpenVPN connection status via OPNsense API and automatically restarts services that are down" \
      org.opencontainers.image.vendor="TekNepal" \
      org.opencontainers.image.source="https://github.com/${GITHUB_REPOSITORY}" \
      org.opencontainers.image.licenses="MIT"

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the monitoring script
COPY monitor.py .

# Create non-root user for security
RUN addgroup -g 1001 -S appuser && \
    adduser -u 1001 -S appuser -G appuser

# Change ownership of the app directory
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Run the script
CMD ["python", "monitor.py"]