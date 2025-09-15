from enum import Enum

from utils import sequence_to_kmer_set

from constants import KMER_COUNT

class NodeType(Enum):
    INNER = "INNER"
    TAXON = "Taxon"
    SEQUENCE = "Sequence"


class Node:
    def __init__(self, label: str, confidence_idx: int, node_type: NodeType):
        self.label = label
        self.confidence_range = (confidence_idx, confidence_idx + 1)
        self.children = []
        self.node_type = node_type

    def add_child(self, child: 'Node'):
        self.children.append(child)

    def increment_confidence_range(self):
        self.confidence_range = (self.confidence_range[0], self.confidence_range[1] + 1)

    def get_last_child_label(self):
        return self.children[-1].label if self.children else None

    def is_inner(self):
        return self.node_type == NodeType.INNER

    def is_taxon(self):
        return self.node_type == NodeType.TAXON

    def is_sequence(self):
        return self.node_type == NodeType.SEQUENCE

    def print(self, depth: int = 0):
        print("   " * depth + f"{self.label} {self.confidence_range}")
        for child in self.children:
            child.print(depth + 1)


class Tree:
    def __init__(self, lineages: list[str], sequences: list[str]):
        self.root = Node("", 0, NodeType.INNER)
        self.lineages = []
        self.num_tips = 0
        self.kmer_map: list[list[int]] = [[] for _ in range(KMER_COUNT)]
        self._build_tree(lineages, sequences)

    def _build_tree(self, lineages: list[str], sequences: list[str]):
        lin_seq_pair = sorted(zip(lineages, sequences))
        for idx, (lineage, sequence) in enumerate(lin_seq_pair):
            self.lineages.append(lineage)
            self.num_tips += 1

            levels = lineage.split(',')
            last_level = len(levels) - 1
            current_node = self.root

            for i, level in enumerate(levels):
                node_type = NodeType.TAXON if i == last_level else NodeType.INNER
                last_label = current_node.get_last_child_label()
                if last_label != level:
                    new_node = Node(level, idx, node_type)
                    current_node.add_child(new_node)
                current_node.confidence_range = (current_node.confidence_range[0], idx + 1)
                current_node = current_node.children[-1]

            current_node.add_child(Node(sequence, idx, NodeType.SEQUENCE))
            current_node.confidence_range = (current_node.confidence_range[0], idx + 1)

            for kmer in sequence_to_kmer_set(sequence):
                self.kmer_map[kmer].append(idx)

    def print(self):
        self.root.print()


# Beispielnutzung:
if __name__ == "__main__":
    lineages = [
        "Bacteria,Proteobacteria,Alphaproteobacteria",
        "Bacteria,Proteobacteria,Betaproteobacteria",
        "Bacteria,Firmicutes,Bacilli",
        "Archaea,Euryarchaeota,Methanobacteria"
    ]

    sequences = [
        "ACGTACGTACGT",
        "ACGTACGTAAAA",
        "TTTTCCCCGGGG",
        "GGGGAAAACCCC"
    ]

    tree = Tree(lineages, sequences)
    tree.print()




