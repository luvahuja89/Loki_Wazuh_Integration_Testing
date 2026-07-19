#!/usr/bin/env python3

import json
import random
import socket
import uuid
from datetime import datetime, timezone

LOG_FILE = "/Users/luvahuja/loki-testing/loki-simulator/logs/loki-sample.log"
mac_hostname = socket.gethostname()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    mac_ip = s.getsockname()[0]
    s.close()
except Exception:
    mac_ip = "127.0.0.1"

levels = ["INFO", "WARNING", "ERROR", "DEBUG", "CRITICAL"]

# Container-specific messages
container_messages = [
    "User authentication succeeded.",
    "User authentication failed.",
    "Application container restarted.",
    "Disk usage exceeded threshold.",
    "CPU utilization above 90%.",
    "Network latency detected.",
    "Pod restarted by Kubernetes.",
    "TLS certificate validation failed.",
    "Configuration updated successfully.",
    "Unauthorized API request detected.",
    "File integrity monitoring event generated.",
    "Loki log stream received.",
    "Container health check passed.",
    "Promtail forwarded new log batch.",
    "Database connection established.",
    "Database connection timeout.",
    "Memory consumption increased.",
    "Security policy applied.",
    "Audit event generated.",
    "Sample Loki event."
]

# Router-specific devices
routers = [
    {"hostname": "router-core-01.prod", "ip": "10.0.1.1"},
    {"hostname": "router-edge-01.prod", "ip": "10.0.2.1"},
    {"hostname": "router-dist-01.prod", "ip": "10.0.3.1"},
    {"hostname": "router-branch-01.office", "ip": "192.168.1.254"}
]

# Router-specific messages
router_messages = [
    "Interface GigabitEthernet0/1 changed state to down",
    "Interface GigabitEthernet0/1 changed state to up",
    "BGP peer 10.255.0.1 established connection",
    "BGP peer 10.255.0.2 connection lost",
    "OSPF process 100 neighbor 10.0.1.2 down: Dead timer expired",
    "SSH login failed for admin from 203.0.113.5",
    "Configured from console by admin on vty0",
    "High CPU utilization (95%) detected on Route Processor",
    "NAT pool exhausted on external interface",
    "IP SLA destination 8.8.8.8 latency exceeded 150ms"
]

with open(LOG_FILE, "a") as f:
    for i in range(1, 21):
        is_router = random.choice([True, False])
        
        if is_router:
            router = random.choice(routers)
            event = {
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "level": random.choice(levels),
                "app": "router-gateway",
                "hostname": router["hostname"],
                "device_name": router["hostname"],
                "source_ip": router["ip"],
                "unique_id": f"LOKI_ROUTER_{router['hostname']}_{i:05d}",
                "tenant": "production",
                "device_type": "router",
                "message": random.choice(router_messages)
            }
        else:
            event = {
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "level": random.choice(levels),
                "app": "grafana-loki",
                "hostname": mac_hostname,
                "device_name": mac_hostname,
                "source_ip": mac_ip,
                "unique_id": f"LOKI_SAMPLE_{mac_hostname}_{mac_ip}_{i:05d}",
                "tenant": "production",
                "cluster": "demo-cluster",
                "namespace": "default",
                "pod": f"sample-pod-{random.randint(1,5)}",
                "container": "grafana-loki",
                "device_type": "container",
                "message": random.choice(container_messages)
            }

        f.write(json.dumps(event))
        f.write("\n")

print("20 Loki/Router sample logs generated successfully with device_name.")
