import re
from distutils.file_util import copy_file
from pathlib import Path

import pytest
from starkware.starknet.definitions.general_config import StarknetChainId

from protostar.cli.signable_command_util import PRIVATE_KEY_ENV_VAR_NAME


@pytest.mark.usefixtures("init")
def test_deploying_contract_with_constructor(
    protostar, devnet_gateway_url, datadir: Path
):
    copy_file(
        src=str(datadir / "contract_with_constructor.cairo"),
        dst="./src/main.cairo",
    )
    protostar(["build"])

    result = protostar(
        [
            "--no-color",
            "deploy",
            "./build/main.json",
            "--inputs",
            "0x42",
            "--gateway-url",
            devnet_gateway_url,
            "--chain-id",
            str(StarknetChainId.TESTNET.value),
        ]
    )

    assert "Deploy transaction was sent" in result
    assert count_hex64(result) == 2


@pytest.mark.usefixtures("init")
@pytest.mark.parametrize("protostar_version", ["0.0.0"])
def test_deploying_contract_with_constructor_and_inputs_defined_in_config_file(
    protostar, devnet_gateway_url, datadir: Path
):
    copy_file(
        src=str(datadir / "contract_with_constructor.cairo"),
        dst="./src/main.cairo",
    )
    copy_file(
        src=str(datadir / "protostar_toml_with_constructor_args.toml"),
        dst="./protostar.toml",
    )
    protostar(["build"])

    result = protostar(
        [
            "--no-color",
            "deploy",
            "./build/main.json",
            "--gateway-url",
            devnet_gateway_url,
            "--chain-id",
            str(StarknetChainId.TESTNET.value),
        ]
    )

    assert "Deploy transaction was sent" in result
    assert count_hex64(result) == 2


@pytest.mark.usefixtures("init")
def test_declaring_contract(protostar, devnet_gateway_url, datadir: Path):
    copy_file(
        src=str(datadir / "contract_with_constructor.cairo"),
        dst="./src/main.cairo",
    )
    protostar(["build"])

    result = protostar(
        [
            "--no-color",
            "declare",
            "./build/main.json",
            "--gateway-url",
            devnet_gateway_url,
            "--chain-id",
            str(StarknetChainId.TESTNET.value),
        ]
    )

    assert "Declare transaction was sent" in result
    assert count_hex64(result) == 2


@pytest.mark.usefixtures("init")
def test_declaring_contract_with_signature(
    protostar, devnet_gateway_url, datadir: Path, signing_credentials, monkeypatch
):
    private_key, account_address = signing_credentials

    copy_file(
        src=str(datadir / "contract_with_constructor.cairo"),
        dst="./src/main.cairo",
    )
    monkeypatch.setenv(PRIVATE_KEY_ENV_VAR_NAME, private_key)

    protostar(["build"])

    result = protostar(
        [
            "--no-color",
            "declare",
            "./build/main.json",
            "--gateway-url",
            devnet_gateway_url,
            "--chain-id",
            str(StarknetChainId.TESTNET.value),
            "--account-address",
            account_address,
        ]
    )

    assert "Declare transaction was sent" in result
    assert count_hex64(result) == 2


def count_hex64(x: str) -> int:
    return len(re.findall(r"0x[0-9a-f]{64}", x))
