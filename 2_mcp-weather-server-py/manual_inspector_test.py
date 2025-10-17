import subprocess
import sys
import time
import webbrowser
from threading import Timer


def open_browser():
    """Open browser after a delay"""
    time.sleep(5)  # Wait for server to fully start
    webbrowser.open('http://localhost:6274')


def main():
    print("🚀 Starting MCP Development Server with Inspector...")
    print("📋 Available Tools:")
    print("   • get-weather: Get current weather for a city")
    print("   • get-forecast: Get 7-day forecast for a city")
    print("")
    print("🧪 Manual Testing Instructions:")
    print("   1. Wait for the server to start completely")
    print("   2. Open http://localhost:6274 in your browser")
    print("   3. Click on 'Tools' tab")
    print("   4. Test different cities with get-weather tool:")
    print("      - Barcelona: {\"city\": \"Barcelona\"}")
    print("      - Rome: {\"city\": \"Rome\"}")
    print("      - Berlin: {\"city\": \"Berlin\"}")
    print("      - Invalid: {\"city\": \"InvalidCity123\"}")
    print("   5. Test forecast with get-forecast tool:")
    print("      - Madrid: {\"city\": \"Madrid\"}")
    print("")
    print("⚠️  Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Schedule browser opening
    browser_timer = Timer(5.0, open_browser)
    browser_timer.start()
    
    try:
        # Start the MCP dev server with editable installation
        result = subprocess.run([
            "uv", "run", "mcp", "dev", "-e", ".", "server.py"
        ], check=False)
        
        if result.returncode != 0:
            print(f"❌ Server failed to start with return code: {result.returncode}")
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
    finally:
        browser_timer.cancel()


if __name__ == "__main__":
    main()
