import socket
import ssl

from config import (
    TAK_HOST,
    TAK_PORT,
    CA_FILE,
    CERT_FILE,
    KEY_FILE,
)

def send_to_tak(cot: str):

    context = ssl.create_default_context(
        cafile=CA_FILE
    )

    context.load_cert_chain(
        certfile=CERT_FILE,
        keyfile=KEY_FILE
    )

    with socket.create_connection(
        (TAK_HOST,TAK_PORT),
        timeout=5
    ) as sock:

        with context.wrap_socket(
            sock,
            server_hostname=TAK_HOST
        ) as tls:

            tls.sendall(
                cot.encode("utf-8") + b"\n"
            )