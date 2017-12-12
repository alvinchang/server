from flask import Flask

from blueprints.printers.views import printer_blueprint
from datastore.users.views import users_blueprint

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Development Server Help')
    parser.add_argument("-d", "--debug", action="store_true", dest="debug_mode",
                        help="run in debug mode (for use with PyCharm)", default=False)
    parser.add_argument("-p", "--port", dest="port",
                        help="port of server (default:%(default)s)", type=int, default=5000)

    cmd_args = parser.parse_args()
    app_options = {"port": cmd_args.port}

    if cmd_args.debug_mode:
        app_options["debug"] = True
        app_options["use_debugger"] = False
        app_options["use_reloader"] = False

    app = Flask(__name__)

    app.register_blueprint(printer_blueprint, url_prefix="/printer")
    app.register_blueprint(users_blueprint, url_prefix="/users")

    app.run(**app_options)
