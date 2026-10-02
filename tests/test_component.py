from kavel_haystack import KavelImageGenerator


def test_roundtrip():
    gen = KavelImageGenerator(aspect_ratio="16:9")
    data = gen.to_dict()
    again = KavelImageGenerator.from_dict(data)
    assert again.aspect_ratio == "16:9"
