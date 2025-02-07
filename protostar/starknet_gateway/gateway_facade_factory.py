from logging import Logger
from pathlib import Path
from typing import Optional

from starknet_py.net.gateway_client import GatewayClient

from protostar.compiler import CompiledContractReader
from protostar.utils import log_color_provider

from .gateway_facade import GatewayFacade


class GatewayFacadeFactory:
    def __init__(
        self,
        project_root_path: Path,
        compiled_contract_reader: CompiledContractReader,
    ) -> None:
        self._project_root_path = project_root_path
        self._compiled_contract_reader = compiled_contract_reader

    def create(self, gateway_client: GatewayClient, logger: Optional[Logger]):
        return GatewayFacade(
            project_root_path=self._project_root_path,
            compiled_contract_reader=self._compiled_contract_reader,
            gateway_client=gateway_client,
            logger=logger,
            log_color_provider=log_color_provider,
        )
