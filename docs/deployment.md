# Deployment Guide

## Production Deployment

### Prerequisites
- Linux server (Ubuntu 20.04+ recommended)
- Python 3.8+
- Node.js 16+
- Reverse proxy (Nginx recommended)
- SSL certificate (Let's Encrypt recommended)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd genaigo
   ```

2. **Install Backend Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

3. **Install Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Build the Frontend**
   ```bash
   cd frontend
   npm run build
   cd ..
   ```

5. **Configure Gmail Integration**
   - Run the setup script: `python backend/setup_gmail.py`
   - Follow the OAuth2 authorization process
   - Verify credentials are stored in `config/gmail.json`

6. **Configure Fetcher Settings**
   - Edit `config/fetcherSettings.json` as needed
   - Set appropriate sender whitelist
   - Configure fetch schedule

### Server Configuration

#### Using systemd (Recommended)

1. **Create Backend Service**
   Create `/etc/systemd/system/genaigo-backend.service`:
   ```ini
   [Unit]
   Description=GenAI Go Backend
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/path/to/genaigo/backend
   ExecStart=/usr/bin/python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   Restart=always
   RestartSec=3

   [Install]
   WantedBy=multi-user.target
   ```

2. **Create Frontend Service**
   Create `/etc/systemd/system/genaigo-frontend.service`:
   ```ini
   [Unit]
   Description=GenAI Go Frontend
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/path/to/genaigo/frontend
   ExecStart=/usr/bin/npm run preview -- --host 127.0.0.1 --port 5173
   Restart=always
   RestartSec=3

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and Start Services**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable genaigo-backend
   sudo systemctl enable genaigo-frontend
   sudo systemctl start genaigo-backend
   sudo systemctl start genaigo-frontend
   ```

#### Using Nginx as Reverse Proxy

1. **Install Nginx**
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. **Create Nginx Configuration**
   Create `/etc/nginx/sites-available/genaigo`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       # Redirect all HTTP to HTTPS
       return 301 https://$server_name$request_uri;
   }

   server {
       listen 443 ssl;
       server_name your-domain.com;

       ssl_certificate /path/to/your/certificate.crt;
       ssl_certificate_key /path/to/your/private.key;

       # Frontend
       location / {
           proxy_pass http://127.0.0.1:5173;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       # Backend API
       location /api/ {
           proxy_pass http://127.0.0.1:8000/api/;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       # Backend health endpoint
       location /health {
           proxy_pass http://127.0.0.1:8000/health;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. **Enable the Site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/genaigo /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

### SSL Certificate (Let's Encrypt)

1. **Install Certbot**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

2. **Obtain Certificate**
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

3. **Auto-renewal**
   Certbot sets up automatic renewal by default. Test with:
   ```bash
   sudo certbot renew --dry-run
   ```

## Docker Deployment (Alternative)

### Using Docker Compose

1. **Create Dockerfile for Backend**
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY backend/requirements.txt .
   RUN pip install -r requirements.txt

   COPY backend/ .

   EXPOSE 8000

   CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Create Dockerfile for Frontend**
   ```dockerfile
   FROM node:16-alpine

   WORKDIR /app

   COPY frontend/package*.json ./
   RUN npm install

   COPY frontend/ .

   RUN npm run build

   EXPOSE 5173

   CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "5173"]
   ```

3. **Create docker-compose.yml**
   ```yaml
   version: '3.8'

   services:
     backend:
       build:
         context: .
         dockerfile: Dockerfile.backend
       ports:
         - "8000:8000"
       volumes:
         - ./config:/app/config
         - ./data:/app/data
       environment:
         - PYTHONPATH=/app

     frontend:
       build:
         context: .
         dockerfile: Dockerfile.frontend
       ports:
         - "5173:5173"
       depends_on:
         - backend
   ```

4. **Deploy**
   ```bash
   docker-compose up -d
   ```

## Monitoring and Maintenance

### Health Checks
- Monitor backend health: `curl http://localhost:8000/health`
- Monitor Gmail integration: `curl http://localhost:8000/api/gmail/health`

### Log Management
- Check systemd logs: `journalctl -u genaigo-backend -f`
- Check application logs in the data directory
- Set up log rotation for large deployments

### Data Backup
- Regularly backup `config/` and `data/` directories
- Store backups securely
- Test restoration procedures periodically

### Updates
1. Pull latest code: `git pull`
2. Update dependencies:
   ```bash
   cd backend && pip install -r requirements.txt
   cd ../frontend && npm install
   ```
3. Rebuild frontend: `npm run build`
4. Restart services:
   ```bash
   sudo systemctl restart genaigo-backend
   sudo systemctl restart genaigo-frontend
   ```

## Security Considerations

### File Permissions
- Restrict access to `config/gmail.json` (contains OAuth tokens)
- Ensure proper ownership of files and directories
- Use dedicated service user for running applications

### Network Security
- Use firewall to restrict unnecessary access
- Keep only required ports open (80, 443)
- Regularly update system and application dependencies

### Regular Maintenance
- Monitor disk space usage
- Check for failed fetch operations in logs
- Verify SSL certificate validity
- Update dependencies regularly