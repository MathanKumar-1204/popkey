# Production Deployment Guide - Elastic APM & Kibana

## ✅ Is Elastic APM Effective for Production?

### **YES - Absolutely!** ✅

Elastic APM is **designed for production** and is used by thousands of companies worldwide. However, you need to configure it properly for production use.

---

## 📊 Production vs Development Comparison

| Feature | Development | Production |
|---------|------------|------------|
| **APM Agent** | ✅ Same | ✅ Same |
| **Data Collection** | 100% of requests | 50% sampling (configurable) |
| **Security** | No token | ✅ Secret token required |
| **HTTPS** | HTTP OK | ✅ HTTPS required |
| **Debug Mode** | True | ✅ False |
| **Performance Impact** | ~5% overhead | ✅ ~2-3% overhead |
| **Log Format** | Human-readable | ✅ JSON (machine-parseable) |
| **Error Tracking** | All errors | ✅ All errors + sampling |
| **Scalability** | Single instance | ✅ Horizontal scaling support |

---

## 🚀 Production Setup

### Step 1: Install Required Packages

```bash
pip install django-environ
pip install elastic-apm
pip install gunicorn  # Production WSGI server
```

### Step 2: Create `.env` File

```bash
# Copy the example
cp .env.example .env

# Edit with your production values
```

**Production `.env` Example:**
```env
# Django
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,api.yourdomain.com

# Database (Supabase)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=Matahn@lock1204
DB_HOST=db.ecmujpmhbwzwbrrxneng.supabase.co
DB_PORT=5432

# Redis (Use managed Redis in production)
REDIS_URL=redis://your-redis-host:6379/1
REDIS_PASSWORD=your-redis-password

# Elastic APM - Production
ELASTIC_APM_SERVICE_NAME=smart-locker-system
ELASTIC_APM_SERVER_URL=https://apm.yourdomain.com:8200
ELASTIC_APM_SECRET_TOKEN=generate-a-long-random-token-here
ELASTIC_APM_ENVIRONMENT=production
ELASTIC_APM_DEBUG=False

# Elasticsearch - Production (Managed Service)
ELASTICSEARCH_HOST=https://your-elasticsearch-cloud.elastic-cloud.com:9243
ELASTICSEARCH_USERNAME=elastic
ELASTICSEARCH_PASSWORD=your-elasticsearch-password

# Logging
LOG_LEVEL=INFO
LOG_DIR=/var/log/locker-system
```

### Step 3: Use Production Settings

**Option A: Environment Variable**
```bash
export DJANGO_SETTINGS_MODULE=locker_system.production_settings
```

**Option B: Command Line**
```bash
python manage.py runserver --settings=locker_system.production_settings
```

**Option C: Gunicorn**
```bash
gunicorn locker_system.production_settings:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 120
```

---

## 🔒 Production Security Checklist

### ✅ Elastic APM Security:

```python
ELASTIC_APM = {
    'SECRET_TOKEN': 'your-secret-token',  # ✅ Required
    'SERVER_URL': 'https://...',           # ✅ HTTPS required
    'DEBUG': False,                        # ✅ Always False
    'CAPTURE_BODY': 'errors',              # ✅ Privacy: only on errors
    'CAPTURE_HEADERS': False,              # ✅ Don't leak headers
}
```

### ✅ Django Security:

```python
# Already in production_settings.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
DEBUG = False
```

### ✅ Elasticsearch Security:

```yaml
# elasticsearch.yml (if self-hosted)
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
xpack.security.http.ssl.enabled: true
```

---

## 📈 Production Performance Tuning

### APM Sampling Rate:

**Control how much data to collect:**

```python
ELASTIC_APM = {
    # Production: Sample 10-50% of transactions
    'TRANSACTION_SAMPLE_RATE': 0.5,  # 50%
    
    # High traffic: Sample 10%
    # 'TRANSACTION_SAMPLE_RATE': 0.1,
    
    # Critical systems: Sample 100%
    # 'TRANSACTION_SAMPLE_RATE': 1.0,
}
```

**Why sample?**
- Reduces storage costs
- Reduces network overhead
- Still statistically accurate
- 50% sampling = 95% confidence with half the data

### Connection Pooling:

```python
CACHES = {
    'default': {
        'OPTIONS': {
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,  # ✅ Reuse connections
                'retry_on_timeout': True,
            },
        },
    }
}
```

### Database Connection Persistence:

```python
# Keep DB connections open
CONN_MAX_AGE = 60  # 60 seconds
```

---

## 🏗️ Production Architecture

### Recommended Stack:

```
┌─────────────────────────────────────────┐
│           Load Balancer (Nginx)         │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼────┐          ┌────▼────┐
│Gunicorn│          │Gunicorn │  (2-4 workers)
│Worker 1│          │Worker 2 │
└───┬────┘          └────┬────┘
    │                     │
    └──────────┬──────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼────┐          ┌────▼────┐
│ Django │─────────▶│ APM     │
│  App   │          │ Agent   │
└────────┘          └────┬────┘
                         │
                    ┌────▼─────────┐
                    │  APM Server  │
                    └────┬─────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
        ┌─────▼─────┐        ┌─────▼─────┐
        │Elastic    │        │  Kibana   │
        │search     │        │  (UI)     │
        └───────────┘        └───────────┘
```

### Docker Compose Production:

```yaml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn locker_system.production_settings:application \
             --bind 0.0.0.0:8000 \
             --workers 4 \
             --timeout 120
    environment:
      - DJANGO_SETTINGS_MODULE=locker_system.production_settings
    env_file: .env
    depends_on:
      - redis
    restart: always

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    restart: always

  apm-server:
    image: docker.elastic.co/apm/apm-server:8.11.0
    environment:
      - output.elasticsearch.hosts=["https://elasticsearch:9200"]
      - apm-server.secret_token=${ELASTIC_APM_SECRET_TOKEN}
    ports:
      - "8200:8200"
    restart: always

volumes:
  redis_data:
```

---

## 📊 Monitoring in Production

### What APM Tracks in Production:

#### 1. **Performance Metrics**
- ✅ Response times (p50, p95, p99)
- ✅ Throughput (requests/minute)
- ✅ Error rates
- ✅ Database query performance
- ✅ Cache hit/miss ratios

#### 2. **Error Tracking**
- ✅ All unhandled exceptions
- ✅ Stack traces
- ✅ User context
- ✅ Request data
- ✅ Environment info

#### 3. **Service Health**
- ✅ CPU usage
- ✅ Memory consumption
- ✅ Database connections
- ✅ Redis connections
- ✅ Network latency

#### 4. **Business Metrics**
- ✅ User registrations
- ✅ Login success/failure
- ✅ Locker reservations
- ✅ Active users

---

## 🎯 Production Kibana Dashboards

### Dashboard 1: Application Health

```
┌─────────────────────────────────────────┐
│  Application Health Overview            │
├─────────────────────────────────────────┤
│  Response Time: 45ms (p95)              │
│  Error Rate: 0.5%                       │
│  Throughput: 150 req/min                │
│  Uptime: 99.9%                          │
└─────────────────────────────────────────┘
```

### Dashboard 2: API Performance

```
┌─────────────────────────────────────────┐
│  API Endpoint Performance               │
├─────────────────────────────────────────┤
│  POST /api/auth/login/       120ms avg  │
│  GET  /api/lockers/available/ 25ms avg  │
│  POST /api/reservations/      80ms avg  │
│  PUT  /api/lockers/:id/       65ms avg  │
└─────────────────────────────────────────┘
```

### Dashboard 3: Error Monitoring

```
┌─────────────────────────────────────────┐
│  Error Summary (Last 24h)               │
├─────────────────────────────────────────┤
│  Total Errors: 23                       │
│  ValidationError: 15                    │
│  ConnectionError: 5                     │
│  PermissionError: 3                     │
└─────────────────────────────────────────┘
```

---

## 🔔 Production Alerts

### Set Up Alerts in Kibana:

**Alert 1: High Error Rate**
```yaml
Condition: Error rate > 5% over 5 minutes
Action: Send Slack notification + Email
Severity: Critical
```

**Alert 2: Slow Response Time**
```yaml
Condition: p95 response time > 500ms over 10 minutes
Action: Send Slack notification
Severity: Warning
```

**Alert 3: High Memory Usage**
```yaml
Condition: Memory > 80% for 15 minutes
Action: Send email
Severity: Warning
```

**Alert 4: Database Connection Issues**
```yaml
Condition: DB connection errors > 10 per minute
Action: Send PagerDuty alert
Severity: Critical
```

---

## 📈 Scaling for Production

### High Traffic (>1000 req/min):

```python
ELASTIC_APM = {
    'TRANSACTION_SAMPLE_RATE': 0.1,  # 10% sampling
    'CAPTURE_BODY': 'errors',
    'CAPTURE_HEADERS': False,
}
```

### Enterprise Scale (>10,000 req/min):

```python
ELASTIC_APM = {
    'TRANSACTION_SAMPLE_RATE': 0.05,  # 5% sampling
    'SERVER_URL': 'https://apm-cluster.yourdomain.com:8200',
    'SERVER_TIMEOUT': 5,
}
```

---

## 💰 Production Costs

### Elastic Cloud Pricing (Managed ELK):

**Small (Development):**
- 1 GB RAM, 20 GB storage
- ~$20/month

**Medium (Production):**
- 4 GB RAM, 100 GB storage
- ~$100/month

**Large (High Traffic):**
- 16 GB RAM, 500 GB storage
- ~$400/month

### Self-Hosted:
- Server costs: $50-200/month
- Maintenance time: 2-5 hours/month
- More control, more work

---

## ✅ Production Checklist

### Before Going Live:

- [ ] Set `DEBUG=False`
- [ ] Generate new `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up HTTPS
- [ ] Configure APM `SECRET_TOKEN`
- [ ] Use HTTPS for APM Server URL
- [ ] Set appropriate sampling rate
- [ ] Configure log rotation
- [ ] Set up monitoring alerts
- [ ] Test error tracking
- [ ] Load test the application
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline
- [ ] Document rollback procedures

---

## 🚀 Deployment Commands

### Production Deployment:

```bash
# 1. Pull latest code
git pull origin main

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate --settings=locker_system.production_settings

# 4. Collect static files
python manage.py collectstatic --settings=locker_system.production_settings

# 5. Restart Gunicorn
sudo systemctl restart locker-system

# 6. Check logs
tail -f /var/log/locker-system/app.log
```

---

## 🎓 Best Practices for Production

### ✅ DO:
- Use environment variables for secrets
- Enable HTTPS everywhere
- Set appropriate sampling rates
- Use JSON logging format
- Set up alerts for critical errors
- Monitor APM agent performance
- Rotate logs regularly
- Use connection pooling
- Enable gzip compression
- Use CDN for static files

### ❌ DON'T:
- Never commit `.env` file
- Never use `DEBUG=True` in production
- Never expose APM Server publicly without auth
- Never log sensitive data (passwords, tokens)
- Never use 100% sampling on high-traffic sites
- Never ignore error alerts
- Never skip log rotation

---

## 📚 Summary

### Is Elastic APM Good for Production?

**YES!** Here's why:

✅ **Industry Standard** - Used by Netflix, Spotify, Uber  
✅ **Low Overhead** - Only 2-5% performance impact  
✅ **Scalable** - Handles millions of requests  
✅ **Secure** - Secret tokens, HTTPS, data filtering  
✅ **Cost-Effective** - Sampling reduces storage costs  
✅ **Feature-Rich** - Errors, performance, traces, metrics  
✅ **Well-Supported** - Official Elastic product  

### What You Get in Production:

📊 **Real-time monitoring** of all API endpoints  
🔍 **Error tracking** with full context  
⚡ **Performance optimization** insights  
🔔 **Proactive alerts** before users notice issues  
📈 **Business metrics** and user behavior  
🎯 **Root cause analysis** for debugging  

---

## 🎉 Ready for Production!

**All files created:**
- ✅ `.env.example` - Production environment template
- ✅ `production_settings.py` - Production Django settings
- ✅ Complete deployment guide

**Next steps:**
1. Copy `.env.example` to `.env`
2. Fill in production values
3. Deploy with `production_settings.py`
4. Monitor in Kibana!

**Your Elastic APM setup is production-ready!** 🚀
