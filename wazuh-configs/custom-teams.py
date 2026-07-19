#!/usr/bin/env python3
# Add this script to /var/ossec/integrations/custom-teams on the Wazuh Manager.
# Make sure to set permissions:
# chmod 750 /var/ossec/integrations/custom-teams
# chown root:wazuh /var/ossec/integrations/custom-teams

import sys
import json
import requests

def main():
    alert_file = sys.argv[1]
    webhook_url = sys.argv[2]
    
    with open(alert_file, 'r') as f:
        alert = json.loads(f.read())
        
    rule_id = alert.get('rule', {}).get('id', 'N/A')
    description = alert.get('rule', {}).get('description', 'N/A')
    level = alert.get('rule', {}).get('level', 0)
    agent_name = alert.get('agent', {}).get('name', 'N/A')
    
    # Extract Loki JSON fields
    data = alert.get('data', {})
    pod = data.get('pod', 'N/A')
    container = data.get('container', 'N/A')
    app = data.get('app', 'N/A')
    log_level = data.get('level', 'N/A')
    message = data.get('message', 'N/A')
    
    # Formulate MS Teams Connector Card
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "FF0000" if level >= 8 else "FFA500" if level >= 5 else "008000",
        "summary": f"Wazuh Loki Alert: {description}",
        "sections": [{
            "activityTitle": f"Wazuh Loki Alert - Rule {rule_id} (Level {level})",
            "activitySubtitle": f"Agent: {agent_name}",
            "facts": [
                {"name": "Description", "value": description},
                {"name": "App / Service", "value": app},
                {"name": "Namespace/Pod", "value": f"{data.get('namespace', 'default')}/{pod}"},
                {"name": "Container", "value": container},
                {"name": "Severity Level", "value": log_level},
                {"name": "Log Message", "value": message}
            ],
            "markdown": True
        }]
    }
    
    headers = {"Content-Type": "application/json"}
    requests.post(webhook_url, json=payload, headers=headers)

if __name__ == '__main__':
    main()
