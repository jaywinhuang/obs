from devobs import app
from devobs.apis import apis

if __name__ == '__main__':
    # Add different router modules(Blueprint).
    app.register_blueprint(apis, url_prefix='/api')
    app.run(debug=True)

