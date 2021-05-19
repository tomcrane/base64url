import base64
import urllib

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

    radios = {
        "simple": None,
        "unicode": None,
        "encodeuri": None
    }
    encoding = request.form.get("encoding")
    if not encoding:
        encoding = "simple"
    radios[encoding] = "checked"

    if iiif_content is not None:
        server_encoded = iiif_content
        try:
            server_plain = decode(iiif_content, encoding)
        except Exception as ex:
            decode_error = repr(ex)

    if operation == "serverEncode":
        server_plain = request.form.get("server-plain")
        try:
            server_encoded = encode(server_plain, encoding)
        except Exception as ex:
            encode_error = repr(ex)

    elif operation == "serverDecode":
        server_encoded = request.form.get("server-encoded")
        try:
            server_plain = decode(server_encoded, encoding)
        except Exception as ex:
            decode_error = repr(ex)

    elif operation == "clientServerEncode":
        client_plain = request.form.get("client-plain")
        server_plain = client_plain
        try:
            server_encoded = encode(server_plain, encoding)
        except Exception as ex:
            encode_error = repr(ex)

    elif operation == "serverClientDecode":
        server_encoded = request.form.get("server-encoded")
        client_encoded = server_encoded
        try:
            server_plain = decode(server_encoded, encoding)
        except Exception as ex:
            decode_error = repr(ex)

    return render_template("index.html", operation=operation, radios=radios,
                           client_plain=client_plain, client_encoded=client_encoded,
                           server_plain=server_plain, server_encoded=server_encoded,
                           encode_error=encode_error, decode_error=decode_error)


def encode(plain_text, method):
    if method == "simple":
        return encode_normal_utf8(plain_text)
    elif method == "unicode":
        # going to do exactly the same here to demonstrate the problem
        return encode_normal_utf8(plain_text)
    elif method == "encodeuri":
        return encode_uri(plain_text)
    else:
        raise Exception("Unknown encoding option " + method)


def decode(content_state, method):
    if method == "simple":
        return decode_normal_utf8(content_state)
    elif method == "unicode":
        # going to do exactly the same here to demonstrate the problem
        return decode_normal_utf8(content_state)
    elif method == "encodeuri":
        return decode_uri(content_state)
    else:
        raise Exception("Unknown encoding option " + method)


def encode_normal_utf8(plain_text):
    binary = plain_text.encode("UTF-8")
    base64url = base64.urlsafe_b64encode(binary)  # this is bytes
    return base64url.decode("UTF-8")


def decode_normal_utf8(content_state):
    binary = base64.urlsafe_b64decode(content_state)
    plain_text = binary.decode("UTF-8")
    return plain_text


def encode_uri(plain_text):
    quoted = urllib.parse.quote(plain_text, safe=',/?:@&=+$#')
    base64url = base64.urlsafe_b64encode(quoted)  # this is bytes
    return base64url.decode("UTF-8")


def decode_uri(content_state):
    binary = base64.urlsafe_b64decode(content_state)
    unquoted = urllib.parse.unquote(binary)
    plain_text = unquoted.decode("UTF-8")
    return plain_text


if __name__ == '__main__':
    app.run()
