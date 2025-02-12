from typing import Any, Callable, Optional

from protostar.starknet import AddressType, Cheatcode


class WarpCheatcode(Cheatcode):
    @property
    def name(self) -> str:
        return "warp"

    def build(self) -> Callable[..., Any]:
        return self.warp

    def warp(
        self,
        blk_timestamp: int,
        target_contract_address: Optional[AddressType] = None,
    ) -> Callable[[], None]:
        target_contract_address = target_contract_address or self.contract_address
        return self.cheaters.block_info.cheat(
            contract_address=target_contract_address,
            block_timestamp=blk_timestamp,
        )
