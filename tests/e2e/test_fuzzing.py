import pytest


@pytest.mark.usefixtures("init")
def test_fuzzing(protostar, copy_fixture):
    copy_fixture("test_fuzz.cairo", "./tests")

    result = protostar(
        ["--no-color", "test", "--seed", "12345678", "tests/test_fuzz.cairo"],
        ignore_exit_code=True,
    )

    # To keep assertions free from having to exclude trailing \n
    result += "\n"

    assert "2 failed, 1 passed, 3 total" in result
    assert "Seed:" in result
    assert "12345678" in result

    assert "[PASS] tests/test_fuzz.cairo" in result
    assert "μ: 18, Md: 18, min: 18, max: 18" in result

    assert "[FAIL] tests/test_fuzz.cairo test_fails_if_big_single_input" in result
    assert (
        """
[falsifying example]:
x = 3618502788666131213697322783095070105623107215331596699973092056135872020480
"""
        in result
    )
    assert f"[test:1]:\nTESTING STDOUT" in result
    assert f"[test:100]:\nTESTING STDOUT" in result

    assert "[FAIL] tests/test_fuzz.cairo test_fails_if_big_many_inputs" in result
    assert (
        """
[falsifying example]:
a = 3618502788666131213697322783095070105623107215331596699973092056135872020480
b = 0
c = 0
"""
        in result
    )
