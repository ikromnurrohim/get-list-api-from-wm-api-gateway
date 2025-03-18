import requests
import jmespath
import csv

# API Configuration
base_url = "http://<ip>:<port>/rest/apigateway/"
operation = ["search/", "policies/", "policyActions?policyActionIds="]

headers = {
    "Authorization": "<basic auth>",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Search API Request Payload
data = {
    "types": ["api"],
    "responseFields": ["apiName", "apiVersion", "gatewayEndpoints", "nativeEndpoint", "policies"]
}

# Make API Request
response = requests.post(base_url + operation[0], headers=headers, json=data)

# Check Response Status
if response.status_code == 200:
    data = response.json()  

    # Open CSV File for Writing
    with open("api_data.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write CSV Headers
        writer.writerow(["API Name", "API Version", "Gateway Endpoints", "Native Endpoints", "Policies ID", "Routing Endpoint"])

        # Iterate Through APIs
        for x in range(len(data["api"])):
            api_name = jmespath.search(f"api[{x}].apiName", data)
            api_version = jmespath.search(f"api[{x}].apiVersion", data)
            native_endpoints = jmespath.search(f"api[{x}].nativeEndpoint[*].uri", data) or []
            gateway_endpoints = jmespath.search(f"api[{x}].gatewayEndpoints", data) or {}
            policies_id = jmespath.search(f"api[{x}].policies", data) or []

            # Convert lists/dicts to strings for CSV
            native_endpoints_str = ", ".join(native_endpoints)
            gateway_endpoints_str = ", ".join(f"{k}: {v}" for k, v in gateway_endpoints.items())
            policies_id_str = ", ".join(policies_id)

            # Check for Policy Enforcement Routing
            routing_endpoint = "N/A"
            if policies_id:
                policy_response = requests.get(f"{base_url}{operation[1]}{policies_id[0]}", headers=headers)
                policy_data = policy_response.json()

                query_policies_routing = "policy.policyEnforcements[?stageKey=='routing'].enforcements[].enforcementObjectId"
                routing_id = jmespath.search(query_policies_routing, policy_data)

                if routing_id:
                    routing_response = requests.get(f"{base_url}{operation[2]}{routing_id[0]}", headers=headers)
                    routing_data = routing_response.json()

                    endpoint_routing = jmespath.search("policyAction[0].parameters[?templateKey=='endpointUri'].values", routing_data)
                    if endpoint_routing:
                        routing_endpoint = endpoint_routing[0]

            # Write Data to CSV
            writer.writerow([api_name, api_version, gateway_endpoints_str, native_endpoints_str, policies_id_str, routing_endpoint])

    print("CSV file 'api_data.csv' has been successfully created!")

else:
    print(f"Error: {response.status_code}")
