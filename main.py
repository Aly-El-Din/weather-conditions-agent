import uvicorn
# Entry point for running the server
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",  # Path to the app (module:object)
        host="127.0.0.1",  # Specify the host
        port=8008,  # Specify the port
        reload=True  # Enable auto-reload for development
    )