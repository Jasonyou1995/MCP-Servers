import subprocess
import time
import requests
import json
from threading import Thread


def start_mcp_dev_server():
    """Start the MCP development server in a subprocess"""
    proc = subprocess.Popen(
        ["uv", "run", "mcp", "dev", "server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return proc


def test_inspector_api():
    """Test the inspector API directly"""
    inspector_url = "http://localhost:6274"
    
    # Wait a moment for the server to start
    time.sleep(3)
    
    try:
        # Test if inspector is accessible
        response = requests.get(f"{inspector_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ MCP Inspector is running at http://localhost:6274")
            print("   You can open this URL in your browser to test the tools!")
            return True
        else:
            print(f"❌ Inspector returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to inspector: {e}")
        return False


def main():
    print("🚀 Starting MCP Development Server with Inspector...")
    
    # Start the server
    server_proc = start_mcp_dev_server()
    
    try:
        # Test the inspector
        success = test_inspector_api()
        
        if success:
            print("\n📋 Available Tools:")
            print("   • get-weather: Get current weather for a city")
            print("   • get-forecast: Get 7-day forecast for a city")
            print("\n🧪 Test Instructions:")
            print("   1. Open http://localhost:6274 in your browser")
            print("   2. Click on 'Tools' tab")
            print("   3. Select 'get-weather' tool")
            print("   4. Enter: {\"city\": \"Barcelona\"}")
            print("   5. Click 'Call Tool' and see results!")
            print("\n⏸️  Server will run for 30 seconds, then terminate...")
            
            # Keep server running for 30 seconds
            time.sleep(30)
        
    finally:
        print("\n🛑 Terminating server...")
        server_proc.terminate()
        server_proc.wait()


if __name__ == "__main__":
    main()
