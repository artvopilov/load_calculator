import multiprocessing

bind = '0.0.0.0:5000'
max_requests = 1000
max_requests_jitter = 50
timeout = 300
workers = multiprocessing.cpu_count() * 2 + 1
