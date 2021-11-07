from app import restore_padding


def test_padding():
    # Examples from https://datatracker.ietf.org/doc/html/rfc4648#section-10
    for (unpadded, padding) in (("", ""),
                                ("Zg", "=="),
                                ("Zm8", "="),
                                ("Zm9v", ""),
                                ("Zm9vYg", "=="),
                                ("Zm9vYmE", "="),
                                ("Zm9vYmFy", "")):
        padded = unpadded + padding
        restored = restore_padding(unpadded)
        result = "SUCCESS" if padded == restored else "FAILURE"
        print("Expecting %s to restore to %s, got %s: %s" % (unpadded, padded, restored, result))


if __name__ == '__main__':
    test_padding()
