# 🚀 AWS Deployment Guide for HR Suite

## 🌟 AWS Hosting Options Overview

### 1. **AWS Elastic Beanstalk (Recommended for Beginners)**
- ✅ Easy deployment and management
- ✅ Auto-scaling and load balancing
- ✅ Health monitoring
- ✅ Rolling deployments
- 💰 **Cost**: ~$10-50/month depending on usage

### 2. **AWS ECS with Fargate (Containerized)**
- ✅ Serverless containers
- ✅ No server management
- ✅ Auto-scaling
- ✅ Pay-per-use
- 💰 **Cost**: ~$15-40/month

### 3. **AWS Lambda + API Gateway (Serverless)**
- ✅ Pay-per-request
- ✅ Auto-scaling
- ✅ No server management
- ⚠️ Requires code adaptation
- 💰 **Cost**: ~$5-20/month

### 4. **AWS EC2 (Full Control)**
- ✅ Complete control
- ✅ Custom configurations
- ⚠️ Requires server management
- 💰 **Cost**: ~$8-30/month

---

## 🎯 Method 1: AWS Elastic Beanstalk (Easiest)

### Prerequisites
- AWS Account
- AWS CLI installed
- EB CLI installed

### Step 1: Install AWS CLI and EB CLI
```bash
# Install AWS CLI
pip install awscli

# Install EB CLI
pip install awsebcli

# Configure AWS credentials
aws configure
```

### Step 2: Prepare Application
```bash
# Create .ebextensions directory
mkdir .ebextensions

# Create configuration file
echo 'option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: app.py
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: "/var/app/current:$PYTHONPATH"
    FLASK_ENV: "production"' > .ebextensions/python.config
```

### Step 3: Deploy to Elastic Beanstalk
```bash
# Initialize EB application
eb init hr-suite --platform python-3.9 --region us-east-1

# Create environment
eb create hr-suite-prod

# Set environment variables
eb setenv MONGODB_URI="your_mongodb_uri" SECRET_KEY="your_secret_key"

# Deploy
eb deploy

# Open in browser
eb open
```

### Step 4: Custom Domain (Optional)
```bash
# Add custom domain in EB console
# Configure Route 53 or your DNS provider
# Enable SSL certificate via AWS Certificate Manager
```

---

## 🐳 Method 2: AWS ECS with Fargate

### Step 1: Create ECS Configuration
```yaml
# ecs-task-definition.json
{
  "family": "hr-suite",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "hr-suite",
      "image": "your-account.dkr.ecr.region.amazonaws.com/hr-suite:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "FLASK_ENV",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "MONGODB_URI",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:hr-suite/mongodb-uri"
        },
        {
          "name": "SECRET_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:hr-suite/secret-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/hr-suite",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Step 2: Build and Push Docker Image
```bash
# Create ECR repository
aws ecr create-repository --repository-name hr-suite

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com

# Build and tag image
docker build -t hr-suite .
docker tag hr-suite:latest your-account.dkr.ecr.us-east-1.amazonaws.com/hr-suite:latest

# Push image
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/hr-suite:latest
```

### Step 3: Deploy ECS Service
```bash
# Register task definition
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json

# Create ECS cluster
aws ecs create-cluster --cluster-name hr-suite-cluster

# Create service
aws ecs create-service \
  --cluster hr-suite-cluster \
  --service-name hr-suite-service \
  --task-definition hr-suite \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}"
```

---

## ⚡ Method 3: AWS Lambda (Serverless)

### Step 1: Install Zappa
```bash
pip install zappa
```

### Step 2: Configure Zappa
```json
# zappa_settings.json
{
    "production": {
        "app_function": "app.app",
        "aws_region": "us-east-1",
        "profile_name": "default",
        "project_name": "hr-suite",
        "runtime": "python3.9",
        "s3_bucket": "hr-suite-deployments",
        "environment_variables": {
            "FLASK_ENV": "production"
        },
        "aws_environment_variables": {
            "MONGODB_URI": "your_mongodb_uri",
            "SECRET_KEY": "your_secret_key"
        },
        "memory_size": 512,
        "timeout_seconds": 30
    }
}
```

### Step 3: Deploy with Zappa
```bash
# Initial deployment
zappa deploy production

# Update deployment
zappa update production

# Get URL
zappa status production
```

---

## 🖥️ Method 4: AWS EC2

### Step 1: Launch EC2 Instance
```bash
# Launch Ubuntu 20.04 LTS instance
# t3.micro for testing, t3.small for production
# Configure security group: HTTP (80), HTTPS (443), SSH (22)
```

### Step 2: Server Setup
```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3 python3-pip nginx git -y

# Clone repository
git clone your-repo-url
cd hr-suite

# Install Python dependencies
pip3 install -r requirements.txt

# Install Gunicorn
pip3 install gunicorn
```

### Step 3: Configure Systemd Service
```bash
# Create service file
sudo nano /etc/systemd/system/hr-suite.service
```

```ini
[Unit]
Description=HR Suite Flask App
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/hr-suite
Environment="PATH=/home/ubuntu/.local/bin"
Environment="MONGODB_URI=your_mongodb_uri"
Environment="SECRET_KEY=your_secret_key"
Environment="FLASK_ENV=production"
ExecStart=/home/ubuntu/.local/bin/gunicorn --workers 3 --bind unix:hr-suite.sock -m 007 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### Step 4: Configure Nginx
```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/hr-suite
```

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/hr-suite/hr-suite.sock;
    }
    
    location /static {
        alias /home/ubuntu/hr-suite/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/hr-suite /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# Start services
sudo systemctl start hr-suite
sudo systemctl enable hr-suite
```

### Step 5: SSL Certificate
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 🗄️ Database Options

### 1. MongoDB Atlas (Recommended)
- ✅ Managed service
- ✅ Global clusters
- ✅ Automatic backups
- 💰 **Cost**: $9+/month

### 2. AWS DocumentDB
- ✅ MongoDB-compatible
- ✅ AWS integration
- ✅ VPC security
- 💰 **Cost**: $200+/month

### 3. Self-hosted MongoDB on EC2
- ✅ Full control
- ⚠️ Requires management
- 💰 **Cost**: $20+/month

---

## 🔒 Security Best Practices

### 1. Environment Variables
```bash
# Use AWS Secrets Manager
aws secretsmanager create-secret \
  --name "hr-suite/mongodb-uri" \
  --description "MongoDB connection string" \
  --secret-string "mongodb+srv://..."

aws secretsmanager create-secret \
  --name "hr-suite/secret-key" \
  --description "Flask secret key" \
  --secret-string "your-secret-key"
```

### 2. IAM Roles and Policies
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": [
        "arn:aws:secretsmanager:*:*:secret:hr-suite/*"
      ]
    }
  ]
}
```

### 3. VPC Configuration
- Private subnets for application
- Public subnets for load balancer
- Security groups with minimal access
- NAT Gateway for outbound traffic

---

## 📊 Monitoring and Logging

### 1. CloudWatch
```bash
# Install CloudWatch agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/amazon_linux/amd64/latest/amazon-cloudwatch-agent.rpm
sudo rpm -U ./amazon-cloudwatch-agent.rpm
```

### 2. Application Insights
- Custom metrics for user activity
- Error tracking and alerting
- Performance monitoring

### 3. Log Aggregation
```python
# Add to app.py
import logging
from pythonjsonlogger import jsonlogger

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
```

---

## 💰 Cost Optimization

### 1. Reserved Instances
- Save up to 75% on EC2 costs
- 1-3 year commitments

### 2. Auto Scaling
```bash
# Configure auto scaling for ECS
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --scalable-dimension ecs:service:DesiredCount \
  --resource-id service/hr-suite-cluster/hr-suite-service \
  --min-capacity 1 \
  --max-capacity 10
```

### 3. CloudFront CDN
- Cache static assets
- Reduce bandwidth costs
- Improve global performance

---

## 🚀 Deployment Automation

### GitHub Actions for CI/CD
```yaml
# .github/workflows/deploy.yml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Deploy to Elastic Beanstalk
        run: |
          pip install awsebcli
          eb deploy hr-suite-prod
```

---

## 📋 Quick Comparison

| Service | Complexity | Cost/Month | Scalability | Management |
|---------|------------|------------|-------------|------------|
| **Elastic Beanstalk** | Low | $10-50 | High | Low |
| **ECS Fargate** | Medium | $15-40 | Very High | Low |
| **Lambda** | Medium | $5-20 | Infinite | None |
| **EC2** | High | $8-30 | Medium | High |

---

## 🎯 Recommended Architecture

### For Small Teams (< 100 users)
- **Hosting**: Elastic Beanstalk
- **Database**: MongoDB Atlas
- **CDN**: CloudFront
- **Monitoring**: CloudWatch

### For Medium Teams (100-1000 users)
- **Hosting**: ECS Fargate
- **Database**: MongoDB Atlas (Dedicated)
- **Load Balancer**: Application Load Balancer
- **CDN**: CloudFront
- **Monitoring**: CloudWatch + Custom metrics

### For Large Teams (1000+ users)
- **Hosting**: ECS Fargate with Auto Scaling
- **Database**: MongoDB Atlas (Multi-region)
- **Caching**: ElastiCache Redis
- **Search**: Amazon OpenSearch
- **CDN**: CloudFront with multiple origins
- **Monitoring**: Full observability stack

---

🎉 **Your HR Suite is ready for AWS deployment!** Choose the method that best fits your technical expertise and requirements.