"""Epidemic gossip protocol for peer-to-peer agent state synchronization."""
import random
from typing import Dict, Any, List, Tuple


class GossipNode:
    def __init__(self, node_id: str):
        self.node_id = node_id
        # State: key -> (value, version, node_origin)
        self._state: Dict[str, Tuple[Any, int, str]] = {}

    def set(self, key: str, value: Any) -> int:
        cur_ver = self._state.get(key, (None, 0, ""))[1]
        new_ver = cur_ver + 1
        self._state[key] = (value, new_ver, self.node_id)
        return new_ver

    def get(self, key: str) -> Any:
        entry = self._state.get(key)
        return entry[0] if entry else None

    def export_digest(self) -> Dict[str, int]:
        """Returns map of key -> version for lightweight exchange."""
        return {k: v[1] for k, v in self._state.items()}

    def exchange_push_pull(self, peer: 'GossipNode') -> Tuple[int, int]:
        """Exchanges state with a peer node. Higher version wins."""
        pulled = 0
        pushed = 0

        # Push to peer
        for k, (val, ver, origin) in self._state.items():
            peer_ver = peer._state.get(k, (None, 0, ""))[1]
            if ver > peer_ver:
                peer._state[k] = (val, ver, origin)
                pushed += 1

        # Pull from peer
        for k, (val, ver, origin) in peer._state.items():
            my_ver = self._state.get(k, (None, 0, ""))[1]
            if ver > my_ver:
                self._state[k] = (val, ver, origin)
                pulled += 1

        return pushed, pulled
