# Gunicorn configuration for Vonesse Photos
# See: https://docs.gunicorn.org/en/stable/settings.html

# Server Socket
bind = "0.0.0.0:8000"

# Workers
workers = 2
worker_class = "sync"
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "vonesse-photos"

# Server hooks
def post_worker_init(worker):
    worker.log.info("Worker initialized (pid=%s)", worker.pid)