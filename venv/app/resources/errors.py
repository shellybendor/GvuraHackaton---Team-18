from http import HTTPStatus
from flask_restful import HTTPException

auth_error_dict = {"message": "Access Denied"}


class NoSuchUser(HTTPException):
    pass


class PasswordIsTooShort(HTTPException):
    pass


class EmailAlreadyTaken(HTTPException):
    pass


class InvalidAPIToken(HTTPException):
    pass


class APITokenExpired(HTTPException):
    pass


class InternalServerError(HTTPException):
    pass


class NoSuchStory(HTTPException):
    pass


class NoSuchEvent(HTTPException):
    pass


class TagAlreadyExists(HTTPException):
    pass


class EventAlreadyExists(HTTPException):
    pass


class StoryAlreadyExists(HTTPException):
    pass


class NotAuthorized(HTTPException):
    pass


class CantParticipateInOwnEvent(HTTPException):
    pass


class NoSuchParticipant(HTTPException):
    pass


errors = {
    "NoSuchUser": {
        "message": "No user was found with the given ID",
        "status": HTTPStatus.NOT_FOUND
    },
    "PasswordIsTooShort": {
        "message": "Given password is shorter than 10 characters",
        "status": HTTPStatus.BAD_REQUEST
    },
    "EmailAlreadyTaken": {
        "message": "This email is taken",
        "status": HTTPStatus.BAD_REQUEST
    },
    "InvalidAPIToken": {
        "message": "Invalid API Token",
        "status": HTTPStatus.UNAUTHORIZED
    },
    "APITokenExpired": {
        "message": "API Token expired",
        "status": HTTPStatus.UNAUTHORIZED
    },
    "InternalServerError": {
        "message": "An internal server error occurred",
        "status": HTTPStatus.INTERNAL_SERVER_ERROR
    },
    "NoSuchStory": {
        "message": "No such story was found",
        "status": HTTPStatus.NOT_FOUND
    },
    "NoSuchEvent": {
        "message": "No such event was found",
        "status": HTTPStatus.NOT_FOUND
    },
    "TagAlreadyExists": {
        "message": "Tag already exists",
        "status": HTTPStatus.SEE_OTHER
    },
    "EventAlreadyExists": {
        "message": "Event already exists",
        "status": HTTPStatus.SEE_OTHER
    },
    "StoryAlreadyExists": {
        "message": "Story already exists",
        "status": HTTPStatus.SEE_OTHER
    },
    "NotAuthorized": {
        "message": "Access Denied",
        "status": HTTPStatus.UNAUTHORIZED
    },
    "CantParticipateInOwnEvent": {
        "message": "You can't participate in your own event",
        "status": HTTPStatus.BAD_REQUEST
    },
    "NoSuchParticipant": {
        "message": "This is not a participant of that event",
        "status": HTTPStatus.BAD_REQUEST
    }
}
