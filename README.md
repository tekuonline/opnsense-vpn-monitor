# OPNsense VPN Monitor

A Docker-based service that monitors OpenVPN connection status via OPNsense API and automatically restarts services that are down.

## Features

- Monitors OpenVPN services using the OPNsense API
- Checks if services have status "connected" and a valid real_address IP
- Automatically restarts down services
- Configurable via environment variables
- Runs continuously in a Docker container
- Multi-platform support (AMD64/ARM64)
- Automated Docker Hub publishing

## Quick Start

### Using Pre-built Docker Image (Recommended)

1. **Get API credentials from OPNsense**:
   - Log into your OPNsense web interface
   - Navigate to **System > Access > Users**
   - Select/create a user for API access
   - Click **Create API key** and download the credentials

2. **Set up the service**:
   ```bash
   # Clone this repository
   git clone https://github.com/tekuonline/opnsense-vpn-monitor.git
   cd opnsense-vpn-monitor

   # Copy and configure environment file
   cp .env.example .env
   # Edit .env with your OPNsense API credentials

   # Start the service
   docker-compose up -d
   ```

3. **Check logs**:
   ```bash
   docker-compose logs -f
   ```

### Manual Docker Run

```bash
docker run -d \
  --name opnsense-vpn-monitor \
  --env-file .env \
  curiohokiest2e/opnsense-vpn-monitor:latest
```

## Development Setup

For development or building from source:

1. Clone this repository
2. Copy the sample environment file: `cp .env.example .env`
3. Edit `.env` with your OPNsense API credentials
4. Build and run: `docker-compose up --build`

**Note**: The `docker-compose.override.yml` file is included for local development and will build the image from source instead of using the pre-built Docker Hub image.

## Production Deployment

For production use:

1. **Security**: Store the `.env` file securely and never commit it to version control
2. **Monitoring**: Set up log aggregation to monitor service health
3. **Updates**: Regularly update the Docker image and monitor for OPNsense API changes
4. **Backup**: Keep backups of your API credentials in a secure location

## Docker Hub & CI/CD

This project uses automated Docker image building and publishing via GitHub Actions. The latest images are available on Docker Hub at `curiohokiest2e/opnsense-vpn-monitor`.

### For Users (Using Pre-built Images)

Simply use the Docker Hub image as shown in the Quick Start section above. The image is automatically updated with the latest code changes.

### For Contributors (Setting up CI/CD)

If you're contributing to this project and want to set up automated publishing:

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

The GitHub Actions workflow automatically:
- Builds multi-platform images (AMD64 + ARM64)
- Pushes to Docker Hub on every push to main/master branch
- Creates versioned tags for releases
- Generates build attestations for security

### Manual Image Building

To build and push manually (for contributors):

```bash
# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 -t curiohokiest2e/opnsense-vpn-monitor:latest --push .

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