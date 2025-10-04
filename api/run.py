from app import create_app
from app.admin import setup_admin

app = create_app()
setup_admin(app)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
