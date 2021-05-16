// The following deals with Unicode strings as well as plain ascii.
// Code is adapted from
// https://developer.mozilla.org/en-US/docs/Web/API/WindowOrWorkerGlobalScope/btoa#unicode_strings
// and
// https://stackoverflow.com/a/51838635

function encode(plainContentState) {
    let binary = toBinary(plainContentState);
    let base64 = btoa(binary);
    let base64url = base64.replace(/=/g, "").replace(/\+/g, "-").replace(/\//g, "_");
    return base64url;
}

function decode(base64ContentState) {
    let base64 = replaceCharsAndPad(base64ContentState);
    let binary = atob(base64);
    let plainText = fromBinary(binary);
    return plainText;
}

function replaceCharsAndPad(input) {
    // Replace non-url compatible chars with base64 standard chars
    input = input.replace(/-/g, '+').replace(/_/g, '/');
    // Pad out with standard base64 required padding characters
    let pad = input.length % 4;
    if (pad) {
        if (pad === 1) {
            throw new Error('InvalidLengthError: Input base64url string is the wrong length to determine padding');
        }
        input += new Array(5 - pad).join('=');
    }
    return input;
}

// convert a Unicode string to a string in which
// each 16-bit unit occupies only one byte
function toBinary(string) {
    const codeUnits = new Uint16Array(string.length);
    for (let i = 0; i < codeUnits.length; i++) {
        codeUnits[i] = string.charCodeAt(i);
    }
    return String.fromCharCode(...new Uint8Array(codeUnits.buffer));
}

function fromBinary(binary) {
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < bytes.length; i++) {
        bytes[i] = binary.charCodeAt(i);
    }
    return String.fromCharCode(...new Uint16Array(bytes.buffer));
}
