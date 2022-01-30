from typing import (
    Any,
    Dict,
    Tuple,
)
from flask import jsonify

HTTPRestResponse = Tuple[str, int]
Payload = Dict[str, Any]


# Base
def http_base_response(status: int, message: str, payload: Payload) -> HTTPRestResponse:

    return jsonify({'status': status, 'message': message, 'payload': payload}), status


# Successful - 2XX
def http_ok(message: str, payload: Payload) -> HTTPRestResponse:

    return http_base_response(200, message, payload)


def http_created(message: str, payload: Payload) -> HTTPRestResponse:

    return http_base_response(201, message, payload)


# Client error - 4XX
def http_bad_request(message: str, payload: Payload) -> HTTPRestResponse:

    return http_base_response(400, message, payload)


def http_unauthorized(message: str, payload: Payload) -> HTTPRestResponse:

    return http_base_response(401, message, payload)


def http_not_found(message: str, payload: Payload) -> HTTPRestResponse:

    return http_base_response(404, message, payload)


def http_unprocessable_entity(message: str, payload: Payload) -> HTTPRestResponse:

    return http_base_response(422, message, payload)


# Server error - 5XX
def http_internal_server_error(message: str, payload: Payload) -> HTTPRestResponse:

    return http_base_response(500, message, payload)
