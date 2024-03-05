import multiprocessing

worker_class = "uvicorn.workers.UvicornWorker"
workers = (multiprocessing.cpu_count() * 2) + 1
log_file = "-"
timeout = 300
keepalive = 2
bind = '0.0.0.0:8000'
max_requests = 10000
max_requests_jitter = 1000
