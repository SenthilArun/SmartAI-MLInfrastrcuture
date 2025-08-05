from flask import Flask, jsonify
import requests
import json
from datetime import datetime

class TestServerAPI:
    def __init__(self):
        # Initialize Flask app
        self.app = Flask(__name__)
        # Set up all routes when the class is created
        self.setup_routes()
    
    def setup_routes(self):
        """
        This method defines all the API endpoints/routes for our application.
        It's called once during initialization to register all routes.
        """
        
        # Route 1: Basic Hello World
        @self.app.route('/api/response', methods=['GET'])
        def server_response():
            """Returns a simple   ping  message"""
            return jsonify({
                "message": " server ping message !",
                "status": "success"
            })
        
        # Route 2: Hello with name parameter
        @self.app.route('/api/server_alert', methods=['GET'])
        def get_alert(name):
            """Returns personalized hello message"""
            return jsonify({
                "message": f"Alert, {name}!",
                "status": "success",
                "name": name
            })
        
        # Route 3: Simulating your metrics example with HTTP request
        @self.app.route('/api/metrics', methods=['GET'])
        def get_current_metrics():
            """Returns real-time infrastructure data (simulated via HTTP)"""
            print("🚀 HTTP Request received at /api/metrics")
            print("📡 Processing request during RUNTIME...")
            
            # This simulates the data you might return
            data = {
                "cpu_usage": "45%",
                "memory_usage": "67%",
                "disk_space": "23GB free",
                "uptime": "5 days, 3 hours",
                "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            }
            
            # Print the metrics data during runtime
            print("📊 RUNTIME METRICS DATA:")
            print(f"   CPU Usage: {data['cpu_usage']}")
            print(f"   Memory Usage: {data['memory_usage']}")
            print(f"   Disk Space: {data['disk_space']}")
            print(f"   Uptime: {data['uptime']}")
            print(f"   Timestamp: {data['timestamp']}")
            print("✅ Sending JSON response back to client\n")
            
            return jsonify(data)
        
        # Route 5: New endpoint that makes HTTP request to get metrics
        @self.app.route('/api/metrics/remote', methods=['GET'])
        def get_remote_metrics():
            """Makes HTTP request to our own metrics endpoint during runtime"""
            print("🌐 Making HTTP request during RUNTIME...")
            
            try:
                # Make HTTP request to our own server
                response = requests.get('http://localhost:9000/api/metrics')
                
                if response.status_code == 200:
                    metrics_data = response.json()
                    
                    print("📥 HTTP Response received:")
                    print(f"   Status Code: {response.status_code}")
                    print("📊 FETCHED METRICS VIA HTTP:")
                    print(f"   CPU Usage: {metrics_data['cpu_usage']}")
                    print(f"   Memory Usage: {metrics_data['memory_usage']}")
                    print(f"   Disk Space: {metrics_data['disk_space']}")
                    print(f"   Uptime: {metrics_data['uptime']}")
                    print(f"   Timestamp: {metrics_data['timestamp']}")
                    
                    return jsonify({
                        "source": "HTTP Request",
                        "method": "GET /api/metrics",
                        "data": metrics_data,
                        "status": "success"
                    })
                else:
                    return jsonify({"error": "Failed to fetch metrics", "status_code": response.status_code})
                    
            except requests.exceptions.ConnectionError:
                return jsonify({
                    "error": "Connection failed - make sure server is running",
                    "message": "Try accessing /api/metrics first"
                })
            except Exception as e:
                return jsonify({"error": str(e)})
        
        # Route 4: POST example
        @self.app.route('/api/hello', methods=['POST'])
        def post_hello():
            """Handles POST requests to hello endpoint"""
            return jsonify({
                "message": "Hello from POST request!",
                "method": "POST"
            })
    
    def run(self, debug=True, port=9000):
        """Start the Flask development server"""
        self.app.run(debug=debug, port=port)

# Usage example
if __name__ == "__main__":
    # Create an instance of our API class
    api = TestServerAPI()
    
    print("Starting .. API server...")
    print("Available endpoints:")
    print("  GET  /api/response          - Basic SERVER response")
    print("  GET  /api/alert             - Alert!")
    print("  GET  /api/metrics           - System metrics (with runtime printing)")
    print("  GET  /api/metrics/remote    - Fetch metrics via HTTP request")
    print("  POST /api/hello             - API via POST")
    print("\nServer running at http://localhost:9000")
    print("\n🔥 RUNTIME DEMO:")
    print("1. Visit: http://localhost:9000/api/metrics")
    print("   → Will print metrics data in terminal during runtime")
    print("2. Visit: http://localhost:9000/api/metrics/remote") 
    print("   → Will make HTTP request and print response data")
    print("\n" + "="*50)
    
    # Start the server
    api.run()

# Code Flow Explanation:
"""
STEP-BY-STEP FLOW:

1. CLASS INITIALIZATION (__init__):
   - Creates Flask app instance: self.app = Flask(__name__)
   - Immediately calls self.setup_routes() to register all endpoints

2. ROUTE REGISTRATION (setup_routes):
   - Uses decorator pattern: @self.app.route('/path', methods=['GET'])
   - Each decorator registers a function as a handler for that URL path
   - Functions are nested inside setup_routes method

3. REQUEST HANDLING:
   - When HTTP request comes in, Flask matches URL to registered route
   - Calls the corresponding function (get_hello, get_current_metrics, etc.)
   - Function processes request and returns JSON response via jsonify()

4. RESPONSE:
   - jsonify() converts Python dict to JSON HTTP response
   - Response sent back to client

WHY THIS PATTERN IS USEFUL:
- Organizes all routes in one place (setup_routes method)
- Keeps route definitions separate from app initialization
- Makes it easy to see all available endpoints at a glance
- Allows for conditional route registration if needed
"""