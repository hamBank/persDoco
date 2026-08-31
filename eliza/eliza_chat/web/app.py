import importlib.resources
import uuid

from flask import Flask, jsonify, render_template, request, session

from ..classic.engine import ClassicEliza
from ..classic.script import load_script
from ..persona import PERSONA_NAME

_SCRIPT_TEXT = importlib.resources.files("eliza_chat.data").joinpath("doctor.txt").read_text()

# In-memory conversation store, keyed by a per-browser session id. Each
# conversation gets its own freshly-parsed Script/ClassicEliza, since a
# Decomp's round-robin reassembly counter is mutable state that must not
# be shared between unrelated conversations.
_conversations = {}


def _new_conversation():
    return ClassicEliza(load_script(_SCRIPT_TEXT))


def _get_or_create_conversation():
    conversation_id = session.get("conversation_id")
    eliza = _conversations.get(conversation_id)
    if eliza is None:
        conversation_id = uuid.uuid4().hex
        session["conversation_id"] = conversation_id
        eliza = _new_conversation()
        _conversations[conversation_id] = eliza
    return eliza


def create_app():
    app = Flask(__name__)
    app.config.setdefault("SECRET_KEY", uuid.uuid4().hex)

    @app.get("/")
    def index():
        return render_template("index.html", persona_name=PERSONA_NAME)

    @app.post("/api/start")
    def start():
        conversation_id = uuid.uuid4().hex
        session["conversation_id"] = conversation_id
        eliza = _new_conversation()
        _conversations[conversation_id] = eliza
        return jsonify(reply=eliza.initial(), ended=False)

    @app.post("/api/chat")
    def chat():
        payload = request.get_json(silent=True) or {}
        message = payload.get("message")
        if not message:
            return jsonify(error="message is required"), 400

        eliza = _get_or_create_conversation()
        reply = eliza.respond(message)
        if reply is None:
            return jsonify(reply=eliza.final(), ended=True)
        return jsonify(reply=reply, ended=False)

    return app


def main():
    create_app().run(debug=True)


if __name__ == "__main__":
    main()
