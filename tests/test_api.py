import socket
import pytest
import ssl
from unittest.mock import patch, MagicMock

from send_to_tak import send_to_tak

from config import (
    TAK_HOST,
    TAK_PORT,
    CA_FILE,
    CERT_FILE,
    KEY_FILE,
)

@patch("send_to_tak.ssl.create_default_context")
@patch("send_to_tak.socket.create_connection")
def test_send_to_tak_connects_to_server(
    mock_create_connection,
    mock_create_default_context
):
    context = MagicMock()
    mock_create_default_context.return_value = context

    socket_mock = MagicMock()

    mock_create_connection.return_value.__enter__.return_value = socket_mock

    tls_mock = MagicMock()

    context.wrap_socket.return_value.__enter__.return_value = tls_mock

    send_to_tak("<event />")

    mock_create_connection.assert_called_once_with(
        (TAK_HOST, TAK_PORT),
        timeout=5
    )

@patch("send_to_tak.ssl.create_default_context")
@patch("send_to_tak.socket.create_connection")
def test_send_to_tak_uses_correct_ca(
    mock_create_connection,
    mock_create_default_context
):
    context = MagicMock()
    mock_create_default_context.return_value = context

    mock_create_connection.return_value.__enter__.return_value = MagicMock()
    context.wrap_socket.return_value.__enter__.return_value = MagicMock()

    send_to_tak("<event />")

    mock_create_default_context.assert_called_once_with(
        cafile=CA_FILE
    )

@patch("send_to_tak.ssl.create_default_context")
@patch("send_to_tak.socket.create_connection")
def test_send_to_tak_loads_client_certificate(
    mock_create_connection,
    mock_create_default_context
):
    context = MagicMock()
    mock_create_default_context.return_value = context

    mock_create_connection.return_value.__enter__.return_value = MagicMock()
    context.wrap_socket.return_value.__enter__.return_value = MagicMock()

    send_to_tak("<event />")

    context.load_cert_chain.assert_called_once_with(
        certfile=CERT_FILE,
        keyfile=KEY_FILE
    )

@patch("send_to_tak.ssl.create_default_context")
@patch("send_to_tak.socket.create_connection")
def test_send_to_tak_uses_hostname_for_tls(
    mock_create_connection,
    mock_create_default_context
):
    context = MagicMock()
    mock_create_default_context.return_value = context

    socket_mock = MagicMock()

    mock_create_connection.return_value.__enter__.return_value = socket_mock

    tls_mock = MagicMock()

    context.wrap_socket.return_value.__enter__.return_value = tls_mock

    send_to_tak("<event />")

    context.wrap_socket.assert_called_once_with(
        socket_mock,
        server_hostname=TAK_HOST
    )

@patch("send_to_tak.ssl.create_default_context")
@patch("send_to_tak.socket.create_connection")
def test_send_to_tak_uses_hostname_for_tls(
    mock_create_connection,
    mock_create_default_context
):
    context = MagicMock()
    mock_create_default_context.return_value = context

    socket_mock = MagicMock()

    mock_create_connection.return_value.__enter__.return_value = socket_mock

    tls_mock = MagicMock()

    context.wrap_socket.return_value.__enter__.return_value = tls_mock

    send_to_tak("<event />")

    context.wrap_socket.assert_called_once_with(
        socket_mock,
        server_hostname=TAK_HOST
    )

@patch("send_to_tak.ssl.create_default_context")
@patch("send_to_tak.socket.create_connection")
def test_send_to_tak_raises_error_when_server_is_unreachable(
    mock_create_connection,
    mock_create_default_context
):

    mock_create_connection.side_effect = ConnectionRefusedError()

    with pytest.raises(ConnectionRefusedError):
        send_to_tak("<event />")

@patch("send_to_tak.ssl.create_default_context")
@patch("send_to_tak.socket.create_connection")
def test_send_to_tak_raises_timeout(
    mock_create_connection,
    mock_create_default_context
):

    mock_create_connection.side_effect = socket.timeout()

    with pytest.raises(socket.timeout):
        send_to_tak("<event />")

@patch("send_to_tak.ssl.create_default_context")
@patch("send_to_tak.socket.create_connection")
def test_send_to_tak_raises_ssl_error(
    mock_create_connection,
    mock_create_default_context
):

    context = MagicMock()
    mock_create_default_context.return_value = context

    socket_mock = MagicMock()
    mock_create_connection.return_value.__enter__.return_value = socket_mock

    context.wrap_socket.side_effect = ssl.SSLError(
        "TLS handshake failed"
    )

    with pytest.raises(ssl.SSLError):
        send_to_tak("<event />")