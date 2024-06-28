from flask import Flask, request, jsonify, make_response
from service_registry import service_registry
from validate_http import method_required
from get_service import *
from post_service import *
from put_service import *
from logger_config import setup_logger  
import hmac
import hashlib

app = Flask(__name__)

setup_logger()(app)

@app.route('/api', methods=['GET', 'POST', 'PUT'])
@method_required
def api_route():
    """
    Route to handle API requests for different services. Supports GET, POST, and PUT methods.

    Returns:
        Response: JSON response containing the result of the service function or an error message.
    """
    service = request.args.get('service')
    
    if service in service_registry:
        service_info = service_registry[service]
        service_func = service_info['func']
        
        try:
            if request.method == 'GET':
                params = request.args.to_dict()
                result = service_func(params)
            elif request.method == 'POST':
                data = request.json
                result = service_func(data)
            elif request.method == 'PUT':
                data = request.json
                result = service_func(data)
                
            return jsonify(result)
        except Exception as e:
            app.logger.error(f'Error processing request: {str(e)}')
            return jsonify({"error": "An error occurred"}), 500
    else:
        app.logger.warning(f'Service not found: {service}')
        return jsonify({"error": "Service not found"}), 404

GITHUB_SECRET = 'randstad'

def verify_signature(payload, signature):
    mac = hmac.new(GITHUB_SECRET.encode(), msg=payload, digestmod=hashlib.sha256)
    return hmac.compare_digest('sha256=' + mac.hexdigest(), signature)

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.get_data()
    signature = request.headers.get('X-Hub-Signature-256')

    if not verify_signature(payload, signature):
        return 'Invalid signature', 403

    event = request.headers.get('X-GitHub-Event')
    if event == 'push':
        subprocess.run(['./deploy.sh'])
        return 'Success', 200

    return 'Wrong event type', 400

if __name__ == '__main__':
    app.run()
# SECRET