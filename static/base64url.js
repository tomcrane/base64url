// The following deals with Unicode strings as well as plain ascii.
// Code is adapted from
// https://developer.mozilla.org/en-US/docs/Web/API/WindowOrWorkerGlobalScope/btoa#unicode_strings
// and
// https://stackoverflow.com/a/51838635

function encodeSimple(plainContentState, noPadding) {
    let base64 = btoa(plainContentState);
    let base64url = base64ToBase64url(base64);
    if(noPadding) base64url = removePadding(base64url);
    return base64url;
}

function decodeSimple(base64url, noPadding) {
    if(noPadding) base64url = restorePadding(base64url);
    let base64 = base64urlToBase64(base64url);
    return atob(base64);
}

function encodeBinary(plainContentState, noPadding) {
    let safeString = toBinary(plainContentState);
    let base64 = btoa(safeString);
    let base64url = base64ToBase64url(base64);
    if(noPadding) base64url = removePadding(base64url);
    return base64url;
}

function decodeBinary(base64url, noPadding) {
    if(noPadding) base64url = restorePadding(base64url);
    let base64 = base64urlToBase64(base64url);
    let decoded = atob(base64);
    return fromBinary(decoded);
}

// Now using xxURIComponent
// https://thisthat.dev/encode-uri-vs-encode-uri-component/
function encodeUriComponentEncode(plainContentState, noPadding) {
    console.log("Encoding URIComponent " + plainContentState);
    let uriEncoded = encodeURIComponent(plainContentState);
    console.log("uriEncoded: " + uriEncoded);
    let base64 = btoa(uriEncoded);
    console.log("base64: " + base64);
    let base64url = base64ToBase64url(base64);
    console.log("base64url: " + base64url);
    if(noPadding) {
        base64url = removePadding(base64url);
        console.log("no padding: " + base64url);
    }
    return base64url;
}

function decodeUriComponentEncode(base64url, noPadding) {
    console.log("Decoding URIComponent " + base64url);
    if(noPadding) {
        base64url = restorePadding(base64url);
        console.log("restored padding: " + base64url);
    }
    let base64 = base64urlToBase64(base64url);
    console.log("base64: " + base64);
    let decodedAtob = atob(base64);
    console.log("atob decoded: " + decodedAtob);
    let uriComponentDecoded = decodeURIComponent(decodedAtob);
    console.log(uriComponentDecoded);
    return uriComponentDecoded;
}

function base64ToBase64url(base64) {
    return base64.replace(/\+/g, "-").replace(/\//g, "_");
}

function removePadding(s) {
    return s.replace(/=/g, "");
}

function base64urlToBase64(base64url) {
    // Replace non-url compatible chars with base64 standard chars
    return base64url.replace(/-/g, '+').replace(/_/g, '/');
}

function restorePadding(s) {
    // The length of the restored string must be a multiple of 4
    let pad = s.length % 4;
    let padding = "";
    if (pad) {
        if (pad === 1) {
            throw new Error('InvalidLengthError: Input base64url string is the wrong length to determine padding');
        }
        s += '===='.slice(0, 4 - pad);
    }
    return s + padding;
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
