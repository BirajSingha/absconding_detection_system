from app import create_app
import sys

print("Initializing app...")
try:
    app = create_app()
    print("App initialized.")
except Exception as e:
    print(f"Error initializing app: {e}")
    sys.exit(1)

if __name__ == '__main__':
    print("Starting server on port 5000...")
    try:
        app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Error running server: {e}")