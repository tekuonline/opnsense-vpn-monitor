# OPNsense VPN Monitor

A Docker-based service that monitors OpenVPN connection status via OPNsense API and automatically restarts services that are down.

## Prerequisites

- OPNsense firewall with API access enabled
- Docker and Docker Compose installed on the target system

## Getting API Credentials

1. Log into your OPNsense web interface
2. Navigate to **System > Access > Users** (`/ui/auth/user`)
3. Select the user you want to use for API access (or create a new one)
4. Click the **Create API key** button
5. Download the API key file - it will contain your `key` and `secret`
6. Use these values for `API_KEY` and `API_SECRET` in your `.env` file

**Note**: Ensure the user has appropriate permissions for OpenVPN service management.

## Configuration

Create a `.env` file in the same directory with your configuration:

```
# OPNsense API Configuration
API_BASE_URL=https://your-opnsense.com
API_KEY=your-api-key-here
API_SECRET=your-api-secret-here
CHECK_INTERVAL=60

# Docker Image (for production use)
DOCKER_IMAGE=yourusername/opnsense-vpn-monitor:latest
```

The service will load these environment variables automatically.

## Quick Start with Docker Hub

The easiest way to run OPNsense VPN Monitor is using the pre-built Docker image from Docker Hub:

```bash
# Pull the latest image
docker pull yourusername/opnsense-vpn-monitor:latest

# Or use the docker-compose.yml (update DOCKER_IMAGE in .env)
echo "DOCKER_IMAGE=yourusername/opnsense-vpn-monitor:latest" >> .env
docker-compose up -d
```

## Development Setup

For development or building from source:

## Production Deployment

For production use:

1. **Security**: Store the `.env` file securely and never commit it to version control
2. **Monitoring**: Set up log aggregation to monitor service health
3. **Updates**: Regularly update the Docker image and monitor for OPNsense API changes
4. **Backup**: Keep backups of your API credentials in a secure location

## Docker Hub & CI/CD

This project includes automated Docker image building and publishing via GitHub Actions:

### Setting up Docker Hub Publishing

1. **Create Docker Hub Repository**:
   - Go to [Docker Hub](https://hub.docker.com) and create a new repository
   - Note your Docker Hub username and repository name

2. **Configure GitHub Secrets**:
   - Go to your GitHub repository Settings > Secrets and variables > Actions
   - Add these secrets:
     - `DOCKERHUB_USERNAME`: Your Docker Hub username
     - `DOCKERHUB_TOKEN`: Your Docker Hub access token (create one in Docker Hub Account Settings > Security)

3. **Update Repository References**:
   - Update `DOCKER_IMAGE` in `.env.example` with your Docker Hub repository
   - Update the GitHub Actions workflow file (`.github/workflows/docker-publish.yml`) if needed

### Automated Builds

The GitHub Actions workflow will automatically:
- Build multi-platform images (AMD64 + ARM64)
- Push to Docker Hub on every push to main/master branch
- Create versioned tags for releases
- Generate build attestations for security

### Manual Image Building

To build and push manually:

```bash
# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 -t yourusername/opnsense-vpn-monitor:latest --push .

# Or use the included script
./build-and-push.sh
```

## Troubleshooting

- **400 Bad Request**: Check API credentials and OPNsense API access
- **Connection errors**: Verify network connectivity to OPNsense
- **Permission errors**: Ensure the API user has OpenVPN service permissions
- **Logs**: Use `docker-compose logs -f` for detailed error information

## API Details

- **Status Check**: POST to `/api/openvpn/service/search_sessions` with Basic Auth
- **Restart Service**: POST to `/api/openvpn/service/restart_service/{id}` with Basic Auth
- **Authentication**: HTTP Basic Auth using API key/secret

## Requirements

- Docker and Docker Compose
- Access to OPNsense API with valid API key/secret
- Network connectivity to OPNsense instance

## Security Notes

- Store API credentials securely, do not commit to version control
- Use strong, unique API credentials
- Regularly rotate API keys
- Ensure the container has network access to your OPNsense instance
- Consider using Docker secrets for sensitive environment variables in production