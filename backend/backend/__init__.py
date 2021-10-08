"""Backend package initializer."""
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask("backend")  # pylint: disable=invalid-name
app.config.from_object('backend.config')

import backend.api  # noqa: E402  pylint: disable=wrong-import-position
import backend.views  # noqa: E402  pylint: disable=wrong-import-position
