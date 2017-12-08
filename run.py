from werkzeug.contrib.fixers import ProxyFix

from devobs import app
from devobs.apis import apis
from devobs.auto_check_balance import auto_check

# Add different router modules(Blueprint).
# blueprint
app.register_blueprint(apis, url_prefix='/api')

if __name__ == '__main__':
    # Server proxy configuration for Gunicorn.
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(debug=True)

    # auto check all accounts
    auto_check()

