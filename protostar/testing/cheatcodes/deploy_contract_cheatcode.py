from typing import Dict, Optional

from protostar.migrator.cheatcodes.migrator_deploy_contract_cheatcode import (
    DeployContractCheatcodeProtocol,
    DeployedContract,
)
from protostar.starknet import Cheatcode, KeywordOnlyArgumentCheatcodeException
from protostar.utils.data_transformer import CairoOrPythonData

from .declare_cheatcode import DeclareCheatcode
from .deploy_cheatcode import DeployCheatcode
from .prepare_cheatcode import PrepareCheatcode


class DeployContractCheatcode(Cheatcode):
    def __init__(
        self,
        syscall_dependencies: Cheatcode.SyscallDependencies,
        declare_cheatcode: DeclareCheatcode,
        prepare_cheatcode: PrepareCheatcode,
        deploy_cheatcode: DeployCheatcode,
    ):
        super().__init__(syscall_dependencies)
        self._declare_cheatcode = declare_cheatcode
        self._prepare_cheatcode = prepare_cheatcode
        self._deploy_cheatcode = deploy_cheatcode

    @property
    def name(self) -> str:
        return "deploy_contract"

    def build(self) -> DeployContractCheatcodeProtocol:
        return self.deploy_contract

    # pylint bug ?
    # pylint: disable=keyword-arg-before-vararg
    def deploy_contract(
        self,
        contract_path: str,
        constructor_args: Optional[CairoOrPythonData] = None,
        *args,
        # pylint: disable=unused-argument
        config: Optional[Dict] = None,
    ) -> DeployedContract:
        if len(args) > 0:
            raise KeywordOnlyArgumentCheatcodeException(self.name, ["config"])
        declared_contract = self._declare_cheatcode.declare(contract_path)
        prepared_contract = self._prepare_cheatcode.prepare(
            declared_contract, constructor_args
        )
        return self._deploy_cheatcode.deploy_prepared(prepared_contract)
