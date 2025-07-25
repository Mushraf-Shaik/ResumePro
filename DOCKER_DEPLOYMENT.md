# Docker Deployment Guide for ResumePro

This guide explains how to deploy your ResumePro Flask application using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose installed
- Gemini API key from Google AI Studio

## Quick Start

### 1. Environment Configuration

Copy the environment template and configure your settings:

```bash
cp .env.docker .env
```

Edit `.env` file and add your actual values:
- `GEMINI_API_KEY`: Your Google Gemini API key
- `SECRET_KEY`: A secure secret key for Flask sessions

### 2. Build and Run with Docker Compose

```bash
# Build and start the application
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

The application will be available at:
- **Application**: http://localhost:5000
- **With Nginx** (production): http://localhost:80

### 3. Manual Docker Build (Alternative)

```bash
# Build the Docker image
docker build -t resumepro .

# Run the container
docker run -d \
  --name resumepro-app \
  -p 5000:5000 \
  -e GEMINI_API_KEY=your_api_key_here \
  -e SECRET_KEY=your_secret_key_here \
  -v $(pwd)/backend/uploads:/app/backend/uploads \
  resumepro
```

## Production Deployment

### With Nginx Reverse Proxy

For production deployment with Nginx:

```bash
# Start with production profile
docker-compose --profile production up -d
```

This will start both the Flask app and Nginx reverse proxy.

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `production` |
| `FLASK_DEBUG` | Enable debug mode | `false` |
| `SECRET_KEY` | Flask secret key | Required |
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `MAX_CONTENT_LENGTH` | Max upload size in bytes | `16777216` (16MB) |
| `UPLOAD_FOLDER` | Upload directory | `uploads` |

### SSL/HTTPS Configuration

1. Obtain SSL certificates and place them in `./ssl/` directory
2. Uncomment the HTTPS server block in `nginx.conf`
3. Update the server name with your domain
4. Restart the containers

## Docker Commands Reference

```bash
# View running containers
docker ps

# View application logs
docker logs resumepro-app

# Execute commands inside container
docker exec -it resumepro-app bash

# Remove all containers and images
docker-compose down --rmi all --volumes

# Rebuild without cache
docker-compose build --no-cache

# Scale the application (multiple instances)
docker-compose up --scale resumepro=3
```

## Health Monitoring

The application includes health checks:

```bash
# Check application health
curl http://localhost:5000/health

# View health status in Docker
docker inspect resumepro-app | grep Health -A 10
```

## Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Find process using port 5000
   netstat -tulpn | grep :5000
   # Kill the process or change port in docker-compose.yml
   ```

2. **Permission issues with uploads**:
   ```bash
   # Fix permissions
   sudo chown -R 1000:1000 backend/uploads
   ```

3. **API key not working**:
   - Verify your Gemini API key is correct
   - Check the `.env` file is properly loaded
   - Ensure no extra spaces in environment variables

4. **Container won't start**:
   ```bash
   # Check logs for errors
   docker-compose logs resumepro
   
   # Debug by running interactively
   docker run -it --rm resumepro bash
   ```

### Performance Tuning

For production, consider:

1. **Gunicorn workers**: Adjust `--workers` in Dockerfile based on CPU cores
2. **Memory limits**: Add memory limits in docker-compose.yml
3. **Nginx caching**: Configure static file caching
4. **Database**: Add PostgreSQL/Redis for session storage

### Backup and Persistence

Important directories to backup:
- `./backend/uploads/` - User uploaded files
- `.env` - Environment configuration

## Security Considerations

1. **Never commit `.env` files** to version control
2. **Use strong SECRET_KEY** in production
3. **Enable HTTPS** for production deployments
4. **Regular security updates** of base images
5. **Firewall configuration** to restrict access

## Monitoring and Logging

### Log Management

```bash
# View real-time logs
docker-compose logs -f resumepro

# Export logs to file
docker-compose logs resumepro > app.log

# Rotate logs (add to crontab)
docker-compose logs --tail=1000 resumepro > /var/log/resumepro.log
```

### Resource Monitoring

```bash
# Monitor resource usage
docker stats resumepro-app

# View detailed container info
docker inspect resumepro-app
```

## Scaling and Load Balancing

For high-traffic deployments:

```yaml
# docker-compose.yml - Add load balancer
services:
  resumepro:
    deploy:
      replicas: 3
    # ... existing configuration
```

This Docker setup provides a robust, scalable deployment solution for your ResumePro application with proper security, monitoring, and production-ready configurations.
