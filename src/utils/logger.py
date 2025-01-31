import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(app):
    # Ensure logs directory exists
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create file handler
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Add handlers to app logger
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    return app.logger
