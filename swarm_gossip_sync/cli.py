"""Command-line interface for Swarm Gossip Sync."""
import argparse
from .gossip import GossipNode

def main():
    parser = argparse.ArgumentParser(description="Swarm Gossip Sync CLI")
    parser.add_argument("--demo", action="store_true", help="Demonstrate gossip protocol sync across 3 nodes")
    args = parser.parse_args()

    n1 = GossipNode("agent_1")
    n2 = GossipNode("agent_2")
    n3 = GossipNode("agent_3")

    n1.set("active_task", "synthesize_code")
    print("Initial Node 1 state:", n1.get("active_task"))
    print("Initial Node 3 state:", n3.get("active_task"))

    print("Running Gossip Round 1: Node 1 <-> Node 2...")
    n1.exchange_push_pull(n2)
    print("Running Gossip Round 2: Node 2 <-> Node 3...")
    n2.exchange_push_pull(n3)

    print("Converged Node 3 state:", n3.get("active_task"))

if __name__ == "__main__":
    main()
