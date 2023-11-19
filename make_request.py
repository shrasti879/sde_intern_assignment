import requests

log_entry = {
    "level": "error",
    "message": "Failed to connect to DB",
    "resourceId": "server-1245",
    "timestamp": "2023-09-15T08:00:00Z",
    "traceId": "abc-xyz-123",
    "spanId": "span-456",
    "commit": "5e5342f",
    "metadata": {
        "parentResourceId": "server-0987"
    }
}

url_ingest = "http://127.0.0.1:3000/ingest"
url_get_logs = "http://127.0.0.1:3000/get_logs"

response_ingest = requests.post(url_ingest, json=log_entry)
print("Log Ingestion Response:", response_ingest.text)

response_get_logs = requests.get(url_get_logs)
print("Get Logs Response:", response_get_logs.text)
