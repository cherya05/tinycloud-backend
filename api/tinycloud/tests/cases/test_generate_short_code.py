from tinycloud.routes.url_mapping import generate_short_code

def test_returns_alphanumeric_code():
    short_code = generate_short_code()
    assert short_code.isalnum

def test_returns_eight_characters():
    short_code = generate_short_code()
    assert len(short_code) == 8