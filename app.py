# Entry point for Render deployments which default to looking for 'app:app'
from backend.app import app

if __name__ == "__main__":
    app.run()
