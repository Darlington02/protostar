import asyncio
from dataclasses import dataclass
from typing import Any, Optional

from starknet_py.net.signer import BaseSigner
from typing_extensions import Protocol

from protostar.starknet import (
    Cheatcode,
    CheatcodeException,
    KeywordOnlyArgumentCheatcodeException,
)
from protostar.starknet_gateway import GatewayFacade
from protostar.starknet_gateway.gateway_facade import CompilationOutputNotFoundException

from ..migrator_contract_identifier_resolver import MigratorContractIdentifierResolver
from .network_config import CheatcodeNetworkConfig, ValidatedCheatcodeNetworkConfig


@dataclass
class DeclaredContract:
    class_hash: int


class DeclareCheatcodeProtocol(Protocol):
    def __call__(
        self, contract_path_str: str, *args, config: Optional[Any] = None
    ) -> DeclaredContract:
        ...


class MigratorDeclareCheatcode(Cheatcode):
    @dataclass
    class Config:
        signer: Optional[BaseSigner] = None
        token: Optional[str] = None

    def __init__(
        self,
        syscall_dependencies: Cheatcode.SyscallDependencies,
        gateway_facade: GatewayFacade,
        migrator_contract_identifier_resolver: MigratorContractIdentifierResolver,
        config: "Config",
    ):
        super().__init__(syscall_dependencies)
        self._gateway_facade = gateway_facade
        self._config = config
        self._migrator_contract_identifier_resolver = (
            migrator_contract_identifier_resolver
        )

    @property
    def name(self) -> str:
        return "declare"

    def build(self) -> DeclareCheatcodeProtocol:
        return self._declare

    def _declare(
        self,
        contract_path_str: str,
        *args,
        config: Optional[CheatcodeNetworkConfig] = None,
    ) -> DeclaredContract:
        contract_identifier = contract_path_str
        if len(args) > 0:
            raise KeywordOnlyArgumentCheatcodeException(self.name, ["config"])

        validated_config = ValidatedCheatcodeNetworkConfig.from_dict(
            config or CheatcodeNetworkConfig()
        )

        compiled_contract_path = self._migrator_contract_identifier_resolver.resolve(
            contract_identifier
        )

        try:
            response = asyncio.run(
                self._gateway_facade.declare(
                    compiled_contract_path=compiled_contract_path,
                    token=self._config.token,
                    wait_for_acceptance=validated_config.wait_for_acceptance,
                    signer=self._config.signer,
                )
            )

            return DeclaredContract(
                class_hash=response.class_hash,
            )

        except CompilationOutputNotFoundException as ex:
            raise CheatcodeException(self, ex.message) from ex
