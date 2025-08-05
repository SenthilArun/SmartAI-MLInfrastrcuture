#!/usr/bin/env python3
"""
SmartAI-MLInfrastructure - Minimal Working Version
Test version to ensure basic functionality
"""

import os
import sys
import time
import json
import logging
import argparse
from datetime import datetime
from flask import Flask, jsonify

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_mock_dcim_server():
    """Create mock DCIM server for testing"""
    app = Flask(__name__)
    
    @app.route('/api/v2/racks/power')
    def get_rack_power():
        import random
        racks = []
        for i in range(1, 4):
            racks.append({
                'id': f'rack-{i:02d}',
                'location': f'Row-{(i-1)//2 + 1}',
                'power_consumption_watts': random.randint(7500, 8500),
                'pdu_id': f'pdu-{i:02d}',
                'pdu_status': 'operational'
            })
        logger.info(f"Mock DCIM: Serving power data for {len(racks)} racks")
        return jsonify({'racks': racks})
    
    @app.route('/nlyte/api/v1/sensors/temperature')
    def get_temperature():
        import random
        sensors = []
        locations = ['rack-01', 'rack-02', 'server-room']
        types = ['ambient', 'supply', 'return']
        
        for i, (loc, sensor_type) in enumerate(zip(locations, types)):
            sensors.append({
                'id': f'temp-{i:02d}',
                'location': loc,
                'type': sensor_type,
                'temperature_celsius': round(random.uniform(20, 30), 1)
            })
        logger.info(f"Mock DCIM: Serving temperature data for {len(sensors)} sensors")
        return jsonify({'sensors': sensors})
    
    @app.route('/nlyte/api/v1/cooling/units')
    def get_cooling_status():
        import random
        units = []
        for i in range(1, 4):
            units.append({
                'id': f'crac-{i:02d}',
                'location': f'Zone-{i}',
                'status': random.choice(['operational', 'operational', 'operational', 'warning']),
                'capacity_kw': 50,
                'current_load_percent': random.randint(60, 85)
            })
        logger.info(f"Mock DCIM: Serving cooling data for {len(units)} units")
        return jsonify({'cooling_units': units})
    
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'Mock DCIM Server',
            'timestamp': datetime.now().isoformat()
        })
    
    return app

def test_basic_functionality():
    """Test basic system functionality"""
    print("🧪 Testing Basic Functionality...")
    
    # Test 1: Python imports
    try:
        import requests
        import yaml
        from flask import Flask
        print("✅ Core imports successful")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test 2: File system
    try:
        os.makedirs('./data', exist_ok=True)
        test_file = './data/test.json'
        with open(test_file, 'w') as f:
            json.dump({'test': 'data'}, f)
        os.remove(test_file)
        print("✅ File system operations successful")
    except Exception as e:
        print(f"❌ File system error: {e}")
        return False
    
    # Test 3: Network capabilities
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))  # Bind to any available port
        port = sock.getsockname()[1]
        sock.close()
        print(f"✅ Network binding successful (test port: {port})")
    except Exception as e:
        print(f"❌ Network error: {e}")
        return False
    
    print("🎉 All basic functionality tests passed!")
    return True

def run_mock_dcim_server(port=8080):
    """Run the mock DCIM server"""
    print(f"🚀 Starting Mock DCIM Server on port {port}...")
    print(f"📡 Power endpoint: http://localhost:{port}/api/v2/racks/power")
    print(f"🌡️  Temperature endpoint: http://localhost:{port}/nlyte/api/v1/sensors/temperature")
    print(f"❄️  Cooling endpoint: http://localhost:{port}/nlyte/api/v1/cooling/units")
    print(f"💓 Health check: http://localhost:{port}/health")
    print(f"⏹️  Press Ctrl+C to stop")
    
    app = create_mock_dcim_server()
    
    try:
        app.run(host='0.0.0.0', port=port, debug=False)
    except KeyboardInterrupt:
        print("\n🛑 Mock DCIM Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

def run_quick_benchmark():
    """Run a quick performance benchmark"""
    print("🏃‍♂️ Running Quick Performance Benchmark...")
    
    # CPU benchmark
    import time
    start_time = time.time()
    
    # Simple CPU intensive task
    result = sum(i * i for i in range(100000))
    cpu_time = time.time() - start_time
    
    print(f"✅ CPU Benchmark: {cpu_time:.4f} seconds (result: {result})")
    
    # Memory benchmark
    import sys
    data = [i for i in range(10000)]
    memory_usage = sys.getsizeof(data)
    
    print(f"✅ Memory Benchmark: {len(data)} items, {memory_usage} bytes")
    
    # Try GPU benchmark if available
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        if gpus:
            for i, gpu in enumerate(gpus):
                print(f"✅ GPU {i}: {gpu.name}, {gpu.temperature}°C, {gpu.load*100:.1f}% util")
        else:
            print("⚠️  No GPUs detected")
    except ImportError:
        print("⚠️  GPUtil not available, skipping GPU benchmark")
    
    print("🎉 Quick benchmark completed!")

def show_system_info():
    """Display system information"""
    print("🖥️  System Information:")
    print(f"   Python: {sys.version}")
    print(f"   Platform: {sys.platform}")
    print(f"   Working Directory: {os.getcwd()}")
    print(f"   Script Path: {os.path.abspath(__file__)}")
    
    # Check installed packages
    try:
        import pkg_resources
        installed_packages = [d.project_name for d in pkg_resources.working_set]
        core_packages = ['flask', 'requests', 'pyyaml', 'prometheus-client', 'torch', 'gputil']
        
        print("📦 Package Status:")
        for package in core_packages:
            if package in installed_packages:
                print(f"   ✅ {package}")
            else:
                print(f"   ❌ {package} (not installed)")
    except Exception as e:
        print(f"   ⚠️  Could not check packages: {e}")

def main():
    """Main entry point with command line interface"""
    parser = argparse.ArgumentParser(
        description='SmartAI-MLInfrastructure System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python SmartInfra.py --mode test           # Test basic functionality
  python SmartInfra.py --mode mock-dcim      # Start mock DCIM server
  python SmartInfra.py --mode benchmark      # Run quick benchmark
  python SmartInfra.py --mode info           # Show system information
        """
    )
    
    parser.add_argument(
        '--mode', 
        choices=['test', 'mock-dcim', 'benchmark', 'info'],
        default='test',
        help='Operation mode (default: test)'
    )
    
    parser.add_argument(
        '--port', 
        type=int, 
        default=8080,
        help='Port for mock DCIM server (default: 8080)'
    )
    
    args = parser.parse_args()
    
    print("🚀 SmartAI-MLInfrastructure System")
    print("=" * 50)
    
    if args.mode == 'test':
        show_system_info()
        print("-" * 50)
        success = test_basic_functionality()
        if not success:
            print("❌ Some tests failed. Check your environment setup.")
            sys.exit(1)
        print("✅ System is ready for full deployment!")
        
    elif args.mode == 'mock-dcim':
        run_mock_dcim_server(args.port)
        
    elif args.mode == 'benchmark':
        run_quick_benchmark()
        
    elif args.mode == 'info':
        show_system_info()
    
    print("\n✨ Done!")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)