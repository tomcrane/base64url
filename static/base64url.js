// The following deals with Unicode strings as well as plain ascii.
// Code is adapted from
// https://developer.mozilla.org/en-US/docs/Web/API/WindowOrWorkerGlobalScope/btoa#unicode_strings
// and
// https://stackoverflow.com/a/51838635

function encodeSimple(plainContentState) {
    let base64 = btoa(plainContentState);
    return replaceCharsToBase64url(base64);
}

function decodeSimple(base64url) {
    let base64 = replaceCharsAndPadFromBase64url(base64url);
    return atob(base64);
}

function encodeBinary(plainContentState) {
    let safeString = toBinary(plainContentState);
    let base64 = btoa(safeString);
    return replaceCharsToBase64url(base64);
}

function decodeBinary(base64url) {
    let base64 = replaceCharsAndPadFromBase64url(base64url);
    let decoded = atob(base64);
    return fromBinary(decoded);
}

// This is deliberately encodeURI rather than encodeURIComponent.
// This is slightly more compact if we are going to base64 anyway.
// https://thisthat.dev/encode-uri-vs-encode-uri-component/
function encodeUriEncode(plainContentState) {
    let uriEncoded = encodeURI(plainContentState);
    let base64 = btoa(uriEncoded);
    return replaceCharsToBase64url(base64);
}

function decodeUriEncode(base64url) {
    let base64 = replaceCharsAndPadFromBase64url(base64url);
    let decoded = btoa(base64);
    return decodeURI(decoded);
}


function replaceCharsToBase64url(base64) {
    return base64.replace(/=/g, "").replace(/\+/g, "-").replace(/\//g, "_");
}

function replaceCharsAndPadFromBase64url(base64url) {
    // Replace non-url compatible chars with base64 standard chars
    let s = base64url.replace(/-/g, '+').replace(/_/g, '/');
    // Pad out with standard base64 required padding characters
    let pad = s.length % 4;
    if (pad) {
        if (pad === 1) {
            throw new Error('InvalidLengthError: Input base64url string is the wrong length to determine padding');
        }
        s += new Array(5 - pad).join('=');
    }
    return s;
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
