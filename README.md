# OPNsense VPN Monitor

A Docker-based service that monitors OpenVPN connection status via OPNsense API and automatically restarts services that are down.

## Features

- Monitors OpenVPN services using the OPNsense API
- Checks if services have status "connected" and a valid real_address IP
- Automatically restarts down services
- Configurable via environment variables
- Runs continuously in a Docker container
- Multi-platform support (AMD64/ARM64)

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Access to OPNsense API with valid API key/secret
- Network connectivity to your OPNsense instance

### Step 1: Get API Credentials from OPNsense

1. Log into your OPNsense web interface
2. Navigate to **System > Access > Users**
3. Select/create a user for API access
4. Click **Create API key** and download the credentials

### Step 2: Set Up Environment Variables

Create a `.env` file in your project directory:

```bash
# OPNsense API base URL
API_BASE_URL=https://your-opnsense-instance.com

# OPNsense API credentials (Basic Auth)
API_KEY=your-api-key-here
API_SECRET=your-api-secret-here

# Check interval in seconds (default: 60)
CHECK_INTERVAL=60
```

### Step 3: Run with Docker Compose

Create a `docker-compose.yml` file:

```yaml
services:
  opnsense-vpn-monitor:
    image: curiohokiest2e/opnsense-vpn-monitor:latest
    container_name: opnsense-vpn-monitor
    env_file:
      - .env
    restart: unless-stopped
```

Start the service:

```bash
docker-compose up -d
```

### Alternative: Run with Docker CLI

```bash
docker run -d \
  --name opnsense-vpn-monitor \
  --env-file .env \
  curiohokiest2e/opnsense-vpn-monitor:latest
```

### Step 4: Verify It's Working

Check the logs to ensure the service is monitoring correctly:

```bash
docker-compose logs -f opnsense-vpn-monitor
```

You should see output like:
```
2024-01-15 10:30:00,123 - INFO - Checking OpenVPN services...
2024-01-15 10:30:00,456 - INFO - Service ovpns1 is UP (connected, IP: 192.168.1.100)
2024-01-15 10:30:00,789 - INFO - All services are running correctly
```

## Configuration

| Environment Variable | Description | Default | Required |
|---------------------|-------------|---------|----------|
| `API_BASE_URL` | Your OPNsense instance URL | - | Yes |
| `API_KEY` | OPNsense API key | - | Yes |
| `API_SECRET` | OPNsense API secret | - | Yes |
| `CHECK_INTERVAL` | Check interval in seconds | 60 | No |

## Troubleshooting

### Common Issues

- **400 Bad Request**: Check your API credentials and ensure the API user has OpenVPN service permissions
- **Connection errors**: Verify network connectivity to your OPNsense instance
- **Permission errors**: Ensure the API user has the necessary permissions for OpenVPN services
- **No services found**: Check that OpenVPN services are configured and running on OPNsense

### Getting Help

1. Check the container logs: `docker-compose logs -f`
2. Verify your `.env` file has correct values
3. Ensure your OPNsense API is accessible from the Docker host
4. Check OPNsense firewall rules allow API access

## Security Notes

- Store API credentials securely, do not commit `.env` to version control
- Use strong, unique API credentials
- Regularly rotate API keys
- Ensure the container has network access to your OPNsense instance
- Consider using Docker secrets for sensitive environment variables in production

## Contributing

We welcome contributions! Here's how you can help:

### How to Contribute

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** and test them thoroughly
4. **Commit your changes**: `git commit -m "Add your descriptive commit message"`
5. **Push to your fork**: `git push origin feature/your-feature-name`
6. **Create a Pull Request** on GitHub

### Pull Request Guidelines

- **Describe your changes** clearly in the PR description
- **Reference any issues** your PR addresses
- **Include tests** if you're adding new functionality
- **Update documentation** if needed
- **Follow the existing code style**
- **Ensure CI/CD passes** before submitting

### Development Setup

For contributors who want to develop or test changes:

1. Clone your fork: `git clone https://github.com/your-username/opnsense-vpn-monitor.git`
2. Copy environment file: `cp .env.example .env`
3. Edit `.env` with your test credentials
4. Build and run: `docker-compose -f docker-compose.override.yml up --build`

The `docker-compose.override.yml` file is configured for development and will build the image from source.

### Reporting Issues

- Use GitHub Issues to report bugs or request features
- Include detailed steps to reproduce the issue
- Provide relevant logs and configuration (without sensitive data)
- Specify your OPNsense version and setup

## License

This project is open source. Please check the repository for license information.