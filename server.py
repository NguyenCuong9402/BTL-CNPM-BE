from app.app import create_app


app = create_app()

if __name__ == '__main__':
    """
    Main Application
    python server.py
    """
    app.run(host="0.0.0.0")
