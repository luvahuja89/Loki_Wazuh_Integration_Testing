# Project Memory: Wazuh + Loki Integration POC

## 1. Project Overview & Metadata
* **Project Name**: Loki + Wazuh Integration Testing
* **GitHub Repository**: [Loki_Wazuh_Integration_Testing](https://github.com/luvahuja89/Loki_Wazuh_Integration_Testing.git)
* **Wazuh Manager Version**: 4.8.2 (running inside Docker container `single-node-wazuh.manager-1`)
* **Mac Agent Name / IP**: `MAC-LOKI-POC-LUV` / `100.100.100.211`
* **Wazuh Manager IP**: `100.100.14.16`

---

## 2. Core Technical Discoveries & Resolutions

### A. JSON Field Parsing & Searchability
* **Problem**: Loki JSON fields were not searchable in the Wazuh Dashboard Discover UI.
* **Resolution**: 
  1. Configured the Mac Wazuh Agent to monitor the log file using `<log_format>json</log_format>` in `ossec.conf`. This parses raw JSON lines on the agent side and sends them as structured fields to the manager.
  2. Refreshed the index pattern (`wazuh-alerts-*`) in **Stack Management** -> **Index Patterns** to force the dashboard to reload the new `data.*` fields.

### B. Rule Conflicts & Dynamic Variable Rendering
* **Problem**: Inside Wazuh rule descriptions, using the variable `$(hostname)` always resolved to the physical agent name (`MAC-LOKI-POC-LUV`) rather than the simulated router hostname (e.g. `router-core-01.prod`). Using `$(data.hostname)` resolved to an empty string because the Wazuh rule evaluation engine uses flat namespaces.
* **Resolution**: Updated the Python simulator to write both `"hostname"` (for database searches) and a new conflict-free field named `"device_name"`. The custom rules now reference `$(device_name)` inside descriptions, which dynamically displays the correct router/container hostname.

### C. Minimal Container Configuration Overrides
* **Problem**: The production Wazuh manager container (`single-node-wazuh.manager-1`) is a minimal image and does not contain editors like `vi` or `nano`.
* **Resolution**: Created configuration files locally on the host server (`/home/luv.ahuja/local_rules.xml`) and copied them directly into the container's rules directory using `docker cp`:
  ```bash
  sudo docker cp /home/luv.ahuja/local_rules.xml single-node-wazuh.manager-1:/var/ossec/etc/rules/local_rules.xml
  ```

---

## 3. Implemented Components & Codebase Files

### A. Log Simulator
* **Location**: [loki_sample_generator.py](file:///Users/luvahuja/loki-testing/loki-simulator/scripts/loki_sample_generator.py)
* **Description**: Randomly generates a 50/50 mix of application container logs (`grafana-loki`) and network device logs (`router-gateway`). Appends correct simulated IPs and device names.

### B. Wazuh Agent configuration
* **Location**: `/Library/Ossec/etc/ossec.conf` (snippet in [agent-ossec-snippet.conf](file:///Users/luvahuja/loki-testing/wazuh-configs/agent-ossec-snippet.conf))
* **Description**: Points the agent to monitor `/Users/luvahuja/loki-testing/loki-simulator/logs/loki-sample.log` with the `json` log format.

### C. Wazuh Custom Rules
* **Location**: `/var/ossec/etc/rules/local_rules.xml` (snippet in [manager-local-rules.xml](file:///Users/luvahuja/loki-testing/wazuh-configs/manager-local-rules.xml))
* **Description**: Custom rules matching the `grafana-loki` and `router-gateway` apps. Maps errors, critical events, restarts, and authentication failures to severity levels `5`, `7`, and `8` for indexing.

---

## 4. Current Testing State & Verification
* **Generator Status**: Verified generating logs successfully.
* **Log Ingestion**: Verified agent reading log file and forwarding.
* **Rule Triggering**: Verified manager evaluating custom rules. Real-time alerts visible inside `/var/ossec/logs/alerts/alerts.json` with correct dynamic descriptions.
