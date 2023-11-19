from flask import Flask, render_template, request, jsonify
from queue import Queue
from threading import Thread

app = Flask(__name__)

log_queue = Queue()


def ingest_log(log_data, logs):
    logs.append(log_data)


@app.route('/ingest', methods=['POST'])
def handle_ingest():
    log_data = request.get_json()
    log_queue.put(log_data)
    return jsonify({'message': 'Log ingestion request received'})


@app.route('/get_logs', methods=['GET'])
def get_logs():
    return jsonify({'logs': logs})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search_logs():
    query = request.args.get('query', '').lower()
    filtered_logs = [log for log in logs if query in log['message'].lower()]
    return jsonify({'logs': filtered_logs})


@app.route('/filter', methods=['GET'])
def filter_logs():
    field = request.args.get('field', '')
    value = request.args.get('value', '')

    filtered_log = next((log for log in logs if field in log and log[field] == value), None)

    if filtered_log:
        return jsonify({'log': filtered_log})
    else:
        return jsonify({'message': 'Log not found'})


def log_worker(logs):
    while True:
        log_data = log_queue.get()
        ingest_log(log_data, logs)
        log_queue.task_done()


if __name__ == '__main__':
    logs = []
    worker = Thread(target=log_worker, args=(logs,))
    worker.daemon = True
    worker.start()

    app.run(port=3000, debug=False)
