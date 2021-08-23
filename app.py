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
    no_padding = True
    if request.form.get("submitCheck", None) == "submitted":
        no_padding = request.form.get("no-padding", None) is not None

    iiif_content = request.args.get("iiif-content")

    radios = {
        "simple": None,
        "unicode": None,
        "encodeuri": None
    }
    encoding = request.form.get("encoding")
    if not encoding:
        encoding = "encodeuri"  # Content State 0.9
    radios[encoding] = "checked"

    if iiif_content is not None:
        server_encoded = iiif_content
        try:
            server_plain = decode(iiif_content, encoding, no_padding)
        except Exception as ex:
            decode_error = repr(ex)

    if operation == "serverEncode":
        server_plain = request.form.get("server-plain")
        try:
            server_encoded = encode(server_plain, encoding, no_padding)
        except Exception as ex:
            encode_error = repr(ex)

    elif operation == "serverDecode":
        server_encoded = request.form.get("server-encoded")
        try:
            server_plain = decode(server_encoded, encoding, no_padding)
        except Exception as ex:
            decode_error = repr(ex)

    elif operation == "clientServerEncode":
        client_plain = request.form.get("client-plain")
        server_plain = client_plain
        try:
            server_encoded = encode(server_plain, encoding, no_padding)
        except Exception as ex:
            encode_error = repr(ex)

    elif operation == "serverClientDecode":
        server_encoded = request.form.get("server-encoded")
        client_encoded = server_encoded
        try:
            server_plain = decode(server_encoded, encoding, no_padding)
        except Exception as ex:
            decode_error = repr(ex)

    chk_no_padding = "checked" if no_padding else ""

    return render_template("index.html", operation=operation,
                           radios=radios, chk_no_padding=chk_no_padding,
                           client_plain=client_plain, client_encoded=client_encoded,
                           server_plain=server_plain, server_encoded=server_encoded,
                           encode_error=encode_error, decode_error=decode_error)


def encode(plain_text, method, no_padding):
    if method == "simple":
        return encode_normal_utf8(plain_text, no_padding)
    elif method == "unicode":
        # going to do exactly the same here to demonstrate the problem
        return encode_normal_utf8(plain_text, no_padding)
    elif method == "encodeuri":
        return encode_uri(plain_text, no_padding)
    else:
        raise Exception("Unknown encoding option " + method)


def decode(content_state, method, no_padding):
    if method == "simple":
        return decode_normal_utf8(content_state, no_padding)
    elif method == "unicode":
        # going to do exactly the same here to demonstrate the problem
        return decode_normal_utf8(content_state, no_padding)
    elif method == "encodeuri":
        return decode_uri(content_state, no_padding)
    else:
        raise Exception("Unknown encoding option " + method)


def encode_normal_utf8(plain_text, no_padding):
    binary = plain_text.encode("UTF-8")
    base64url = base64.urlsafe_b64encode(binary)  # this is bytes
    utf8_decoded = base64url.decode("UTF-8")
    if no_padding:
        utf8_decoded = remove_padding(utf8_decoded)
    return utf8_decoded


def decode_normal_utf8(content_state, no_padding):
    if no_padding:
        content_state = restore_padding(content_state)
    binary = base64.urlsafe_b64decode(content_state)
    plain_text = binary.decode("UTF-8")
    return plain_text


def encode_uri(plain_text, no_padding):
    quoted = urllib.parse.quote(plain_text, safe=',/?:@&=+$#')
    binary = quoted.encode("UTF-8")
    base64url = base64.urlsafe_b64encode(binary)  # this is bytes
    utf8_decoded = base64url.decode("UTF-8")
    if no_padding:
        utf8_decoded = remove_padding(utf8_decoded)
    return utf8_decoded


def decode_uri(content_state, no_padding):
    if no_padding:
        content_state = restore_padding(content_state)
    binary = base64.urlsafe_b64decode(content_state)
    plain_text = binary.decode("UTF-8")
    unquoted = urllib.parse.unquote(plain_text)
    return unquoted


# Padding
# base64url spec says:
# The pad character "=" is typically percent-encoded when used in an URI, but if the data length is known
# implicitly, this can be avoided by skipping the padding.
def remove_padding(s):
    return s.replace("=", "")


def restore_padding(s):
    pad = len(s) % 4
    padding = ""
    if pad:
        if pad == 1:
            raise Exception("InvalidLengthError: Input base64url string is the wrong length to determine padding")
        padding = "=" * (5 - pad)
    return s + padding


if __name__ == '__main__':
    app.run()
