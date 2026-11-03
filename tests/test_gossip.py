"""Unit tests for GossipNode."""
import unittest
from swarm_gossip_sync.gossip import GossipNode

class TestGossipNode(unittest.TestCase):
    def test_single_node_state(self):
        n = GossipNode("n1")
        ver = n.set("task", "clean")
        self.assertEqual(ver, 1)
        self.assertEqual(n.get("task"), "clean")

    def test_bidirectional_sync(self):
        n1 = GossipNode("n1")
        n2 = GossipNode("n2")
        n1.set("key1", "val1")
        n2.set("key2", "val2")

        n1.exchange_push_pull(n2)
        self.assertEqual(n1.get("key2"), "val2")
        self.assertEqual(n2.get("key1"), "val1")

    def test_higher_version_wins(self):
        n1 = GossipNode("n1")
        n2 = GossipNode("n2")
        n1.set("status", "initial")
        n1.exchange_push_pull(n2)

        # n2 updates status to newer version
        n2.set("status", "updated")
        n2.exchange_push_pull(n1)
        self.assertEqual(n1.get("status"), "updated")

if __name__ == "__main__":
    unittest.main()
