import socket
import ssl

TAK_HOST = "takserver.test"
TAK_PORT = 8089

CA_FILE = "/home/kaftan/Documents/VS_Code/TAK_NSK_API_01/NSK-API-01-trusted.pem"
CERT_FILE = "/home/kaftan/Documents/VS_Code/TAK_NSK_API_01/NSK-API-01.pem"
KEY_FILE = "/home/kaftan/Documents/VS_Code/TAK_NSK_API_01/NSK-API-01.key"

pwd = "1wdf2345AQ!>sdq1FO2"

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

            tls.sandall(
                cot.encode("utf-8") + b"\n"
            )