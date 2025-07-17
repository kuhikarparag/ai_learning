# Deployment Guide for PR Analyzer & Fixer

This guide provides detailed instructions for deploying the PR Analyzer & Fixer application in various environments.

## Quick Start (Local Development)

```bash
cd pr-analyzer
python -m venv venv
venv\Scripts\activate


source venv/bin/activate
python src/main.py
```

Access the application at `http://localhost:5001`

## Environment Variables

Create a `.env` file in the project root (optional):

```bash
# GitHub Integration (Optional)
GITHUB_TOKEN=ghp_your_github_token_here

# Gemini AI Integration (Optional)
GEMINI_API_KEY=your_gemini_api_key_here

# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your_secret_key_here
```

## Production Deployment

### Option 1: Using Gunicorn (Recommended)

1. **Install Gunicorn**:
   ```bash
   pip install gunicorn
   ```

2. **Create Gunicorn configuration** (`gunicorn.conf.py`):
   ```python
   bind = "0.0.0.0:5001"
   workers = 4
   worker_class = "sync"
   timeout = 120
   keepalive = 2
   max_requests = 1000
   max_requests_jitter = 100
   preload_app = True
   ```

3. **Run with Gunicorn**:
   ```bash
   gunicorn -c gunicorn.conf.py src.main:app
   ```

### Option 2: Using Docker

1. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY src/ ./src/
   COPY . .

   EXPOSE 5001

   CMD ["gunicorn", "-b", "0.0.0.0:5001", "src.main:app"]
   ```

2. **Build and run**:
   ```bash
   docker build -t pr-analyzer .
   docker run -p 5001:5001 -e GITHUB_TOKEN=your_token pr-analyzer
   ```

### Option 3: Nginx Reverse Proxy

1. **Nginx configuration** (`/etc/nginx/sites-available/pr-analyzer`):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5001;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       location /static {
           alias /path/to/pr-analyzer/src/static;
           expires 1y;
           add_header Cache-Control "public, immutable";
       }
   }
   ```

2. **Enable the site**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/pr-analyzer /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

## Cloud Platform Deployment

### Heroku

1. **Create Procfile**:
   ```
   web: gunicorn src.main:app
   ```

2. **Deploy**:
   ```bash
   heroku create your-app-name
   heroku config:set GITHUB_TOKEN=your_token
   heroku config:set GEMINI_API_KEY=your_key
   git push heroku main
   ```

### AWS EC2

1. **Launch EC2 instance** (Ubuntu 22.04 recommended)
2. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx
   ```
3. **Deploy application**:
   ```bash
   git clone your-repo
   cd pr-analyzer
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. **Configure systemd service** (`/etc/systemd/system/pr-analyzer.service`):
   ```ini
   [Unit]
   Description=PR Analyzer Flask App
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/pr-analyzer
   Environment=PATH=/home/ubuntu/pr-analyzer/venv/bin
   ExecStart=/home/ubuntu/pr-analyzer/venv/bin/gunicorn -c gunicorn.conf.py src.main:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
5. **Start service**:
   ```bash
   sudo systemctl enable pr-analyzer
   sudo systemctl start pr-analyzer
   ```

### Google Cloud Platform

1. **Create app.yaml**:
   ```yaml
   runtime: python311

   env_variables:
     GITHUB_TOKEN: your_token
     GEMINI_API_KEY: your_key

   automatic_scaling:
     min_instances: 1
     max_instances: 10
   ```

2. **Deploy**:
   ```bash
   gcloud app deploy
   ```

## Security Considerations

### Environment Variables
- Never commit API keys to version control
- Use environment variables or secret management services
- Rotate keys regularly

### HTTPS
- Always use HTTPS in production
- Configure SSL certificates (Let's Encrypt recommended)
- Update Nginx configuration for SSL

### Firewall
- Restrict access to necessary ports only
- Use security groups (AWS) or firewall rules
- Consider VPN access for internal tools

## Monitoring and Logging

### Application Logs
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
```

### Health Check Endpoint
Add to `src/main.py`:
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
```

### Monitoring Tools
- **Uptime monitoring**: UptimeRobot, Pingdom
- **Application monitoring**: New Relic, DataDog
- **Log aggregation**: ELK Stack, Splunk

## Performance Optimization

### Caching
- Implement Redis for API response caching
- Cache GitHub API responses
- Use CDN for static assets

### Database Optimization
- Use connection pooling
- Implement database indexing
- Consider PostgreSQL for production

### Load Balancing
- Use multiple application instances
- Implement load balancer (AWS ALB, Nginx)
- Consider auto-scaling

## Backup and Recovery

### Database Backup
```bash
# SQLite backup
cp src/database/app.db backups/app_$(date +%Y%m%d_%H%M%S).db
```

### Application Backup
- Version control with Git
- Regular code backups
- Environment configuration backup

## Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   sudo lsof -i :5001
   sudo kill -9 <PID>
   ```

2. **Permission denied**:
   ```bash
   sudo chown -R $USER:$USER /path/to/pr-analyzer
   chmod +x src/main.py
   ```

3. **Module not found**:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **GitHub API rate limit**:
   - Set GITHUB_TOKEN environment variable
   - Use authenticated requests

5. **Gemini API errors**:
   - Verify GEMINI_API_KEY is correct
   - Check API quota and billing

### Log Analysis
```bash
# Application logs
tail -f /var/log/pr-analyzer/app.log

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# System logs
journalctl -u pr-analyzer -f
```

## Scaling Considerations

### Horizontal Scaling
- Use load balancer
- Implement session storage (Redis)
- Database clustering

### Vertical Scaling
- Increase server resources
- Optimize application performance
- Use caching strategies

### Microservices
- Separate PR analysis service
- Dedicated Gemini API service
- Independent scaling

## Maintenance

### Regular Tasks
- Update dependencies monthly
- Monitor security vulnerabilities
- Review and rotate API keys
- Database maintenance and cleanup
- Log rotation and cleanup

### Updates
```bash
# Update application
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart pr-analyzer
```

This deployment guide covers most common scenarios. Adjust configurations based on your specific requirements and infrastructure.

