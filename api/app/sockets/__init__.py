from flask import Blueprint


sockets = Blueprint("sockets", __name__)


from app.sockets import private_chats, group_chats

