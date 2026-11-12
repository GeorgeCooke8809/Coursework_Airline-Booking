import logging
import os
from datetime import datetime

# * Setting up logging
root_logger = logging.getLogger()
root_logger.handlers.clear()

now = datetime.now().strftime("%d.%m.%Y-%H.%M.%S")

log_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(level=logging.INFO, filename=os.path.join(log_dir, f"{now}.log"), filemode="w", format="%(asctime)s - %(levelname)s : %(funcName)s : %(lineno)d - %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logging.getLogger().addHandler(stream_handler)

from frontend import create_app

if __name__ == "__main__":
    logging.info("App starting...")

    app = create_app()

    app.run(host="0.0.0.0", debug=True, port=5000, use_reloader=False)