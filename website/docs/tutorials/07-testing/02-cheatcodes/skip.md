# `skip`
```python
def skip(reason: Optional[str] = None) -> None:
```
Skip a test.

:::warning
This cheatcode is only available in test's setup.
:::

```cairo
%lang starknet

@external
func setup_function() {
    %{ skip("Reason") %} // <-- ok
    return ();
}

@external
func test_function() {
    // %{ skip("Reason") %} <-- won't work
    return ();
}

@external
func __setup__() {
    // %{ skip("Reason") %} <-- won't work
    return ();
}
```
