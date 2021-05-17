import base64
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    # Our four textarea contents
    client_plain = ""
    client_encoded = ""
    server_plain = ""
    server_encoded = ""
    encode_error = ""
    decode_error = ""
    operation = request.form.get("operation")

    iiif_content = request.args.get("iiif-content")
    unicode_aware = request.form.get("chk-unicode")
    checked = ""
    if unicode_aware:
        checked = "checked"

    if iiif_content is not None:
        server_encoded = iiif_content
        try:
            server_plain = decode(iiif_content)
        except Exception as ex:
            decode_error = repr(ex)

    if operation == "serverEncode":
        server_plain = request.form.get("server-plain")
        try:
            server_encoded = encode(server_plain)
        except Exception as ex:
            encode_error = repr(ex)

    elif operation == "serverDecode":
        server_encoded = request.form.get("server-encoded")
        try:
            server_plain = decode(server_encoded)
        except Exception as ex:
            decode_error = repr(ex)

    elif operation == "clientServerEncode":
        client_plain = request.form.get("client-plain")
        server_plain = client_plain
        try:
            server_encoded = encode(server_plain)
        except Exception as ex:
            encode_error = repr(ex)

    elif operation == "serverClientDecode":
        server_encoded = request.form.get("server-encoded")
        client_encoded = server_encoded
        try:
            server_plain = decode(server_encoded)
        except Exception as ex:
            decode_error = repr(ex)

    return render_template("index.html", operation=operation, checked=checked,
                           client_plain=client_plain, client_encoded=client_encoded,
                           server_plain=server_plain, server_encoded=server_encoded,
                           encode_error=encode_error, decode_error=decode_error)


def encode(plain_text):
    binary = plain_text.encode("UTF-8")
    base64url = base64.urlsafe_b64encode(binary)  # this is bytes
    return base64url.decode("UTF-8")


def decode(content_state):
    binary = base64.urlsafe_b64decode(content_state)
    plain_text = binary.decode("UTF-8")
    return plain_text


if __name__ == '__main__':
    app.run()
