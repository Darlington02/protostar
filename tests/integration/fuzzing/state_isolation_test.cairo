%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin

@storage_var
func balance() -> (res: felt) {
}

@external
func __setup__{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() {
    %{ max_examples(3) %}
    balance.write(100);
    return ();
}

@external
func test_storage_var{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(a) {
    let (read) = balance.read();
    assert read = 100;

    balance.write(read + 1);

    return ();
}
