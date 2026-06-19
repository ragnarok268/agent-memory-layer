from app import format_profile


def test_format_profile_trims_input():
    assert format_profile(" Ada ", " Engineer ") == "Ada - Engineer"
