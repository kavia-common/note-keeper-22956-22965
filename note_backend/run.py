from app import app

if __name__ == "__main__":
    # Enable debug autoreload for development convenience
    app.run(host="0.0.0.0", port=3001, debug=True)
