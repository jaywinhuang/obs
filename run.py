from devobs import app
from devobs.apis import apis
from werkzeug.contrib.fixers import ProxyFix

if __name__ == '__main__':
    # Add different router modules(Blueprint).
    # blueprint
    app.register_blueprint(apis, url_prefix='/api')

    # Server proxy configuration for Gunicorn.
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(debug=True)

