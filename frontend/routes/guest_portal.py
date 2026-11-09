from flask import Blueprint, redirect, render_template, session
import logging

LOGGER = logging.getLogger(__name__)

guest_portal = Blueprint("pages", __name__)

LOGGER.info("Website blueprint created")