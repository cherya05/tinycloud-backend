import time
import psutil
from flask import Blueprint, Response, request, g 
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Gauge, Histogram

metrics_bp = Blueprint("metrics", __name__)

cpu_usage = Gauge("cpu_usage_percent", "CPU Usage")
memory_usage = Gauge("memory_usage_percent", "Memory Usage")
http_requests_total = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "path", "status"]
)
http_requests_duration_seconds = Histogram(
    "http_requests_duration_seconds",
    "HTTP duration in seconds",
    ["method", "path"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
)

def init_metrics(app):
    @app.before_request
    def before_request():
        g.start_time = time.time()

    @app.after_request       
    def after_request(response):
        if request.path == "/metrics":
            return response
        
        duration = time.time() - g.start_time

        http_requests_total.labels(
            method=request.method,
            path=request.path,
            status=response.status_code,
        ).inc()

        http_requests_duration_seconds.labels(
            method=request.method,
            path=request.path
        ).observe(duration)

        return response


@metrics_bp.route("/metrics")
def metrics():
    cpu_usage.set(psutil.cpu_percent())
    memory_usage.set(psutil.virtual_memory().percent)
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
