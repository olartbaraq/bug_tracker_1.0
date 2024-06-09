from flask import Blueprint, render_template

bp = Blueprint("main", __name__)


def test_home_page():
    """test if homepage retuns the exact html file"""
    assert render_template("home.html")
