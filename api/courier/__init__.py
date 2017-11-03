#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint

courier_bp = Blueprint('courier', __name__)

from . import views  # noqa
