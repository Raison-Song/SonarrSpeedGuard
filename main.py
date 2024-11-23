import asyncio
import threading

from flask import Flask

import handler.auto_delete_task
import utils.config
from handler.web_ui import main_routes


def run_async_handler():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(handler.auto_delete_task.handler())


def main():
    utils.config.load_config()

    background_thread = threading.Thread(target=run_async_handler, daemon=True)
    background_thread.start()

    app.run(debug=True)


app = Flask(__name__)
app.register_blueprint(main_routes)

if __name__ == "__main__":
    main()
