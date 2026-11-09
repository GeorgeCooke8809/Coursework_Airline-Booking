from flask import Blueprint, jsonify, request, session
from datetime import datetime
import logging

LOGGER = logging.getLogger(__name__)

api = Blueprint("api", __name__)

LOGGER.info("API blueprint created")