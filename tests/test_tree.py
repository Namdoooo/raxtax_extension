import unittest
from tree import Tree
from tree import NodeType

class TestTree(unittest.TestCase):
    def setUp(self):
        self.lineages = [
            "Bacteria,Proteobacteria,Alphaproteobacteria",
            "Bacteria,Proteobacteria,Betaproteobacteria",
            "Bacteria,Firmicutes,Bacilli",
            "Archaea,Euryarchaeota,Methanobacteria"
        ]

        self.sequences = [
            "ACGTACGTACGT",
            "ACGTACGTAAAA",
            "TTTTCCCCGGGG",
            "GGGGAAAACCCC"
        ]

        self.tree = Tree(self.lineages, self.sequences)

    def test_num_tips(self):
        self.assertEqual(self.tree.num_tips, len(self.lineages))

    def test_lineages(self):
        self.assertEqual(len(self.tree.lineages), len(self.lineages))
        self.assertEqual(set(self.tree.lineages), set(self.lineages))

    def test_tree_structure(self):
        # ┌── root (0–4)
        root = self.tree.root
        self.assert_node(root, "", NodeType.INNER, 2, (0, 4))

        # │   ┌── Archaea (0–1)
        archaea = root.children[0]
        self.assert_node(archaea, "Archaea", NodeType.INNER, 1, (0, 1))

        # │   │   └── Euryarchaeota (0–1)
        eury = archaea.children[0]
        self.assert_node(eury, "Euryarchaeota", NodeType.INNER, 1, (0, 1))

        # │   │       └── Methanobacteria (0–1)
        methano = eury.children[0]
        self.assert_node(methano, "Methanobacteria", NodeType.TAXON, 1, (0, 1))

        # │   │           └── (sequence) Methanobacteria (0–1)
        self.assert_node(methano.children[0], "GGGGAAAACCCC", NodeType.SEQUENCE, 0, (0, 1))

        # │   └── Bacteria (1–4)
        bacteria = root.children[1]
        self.assert_node(bacteria, "Bacteria", NodeType.INNER, 2, (1, 4))

        # │       ├── Firmicutes (1–2)
        firmi = bacteria.children[0]
        self.assert_node(firmi, "Firmicutes", NodeType.INNER, 1, (1, 2))

        # │       │   └── Bacilli (1–2)
        bacilli = firmi.children[0]
        self.assert_node(bacilli, "Bacilli", NodeType.TAXON, 1, (1, 2))

        # │       │       └── (sequence) Bacilli (1–2)
        self.assert_node(bacilli.children[0], "TTTTCCCCGGGG", NodeType.SEQUENCE, 0, (1, 2))

        # │       └── Proteobacteria (2–4)
        proteo = bacteria.children[1]
        self.assert_node(proteo, "Proteobacteria", NodeType.INNER, 2, (2, 4))

        # │           ├── Alphaproteobacteria (2–3)
        alpha = proteo.children[0]
        self.assert_node(alpha, "Alphaproteobacteria", NodeType.TAXON, 1, (2, 3))

        # │           │   └── (sequence) Alphaproteobacteria (2–3)
        self.assert_node(alpha.children[0], "ACGTACGTACGT", NodeType.SEQUENCE, 0, (2, 3))

        # │           └── Betaproteobacteria (3–4)
        beta = proteo.children[1]
        self.assert_node(beta, "Betaproteobacteria", NodeType.TAXON, 1, (3, 4))

        # │               └── (sequence) Betaproteobacteria (3–4)
        self.assert_node(beta.children[0], "ACGTACGTAAAA", NodeType.SEQUENCE, 0, (3, 4))

    def assert_node(self, node, label, node_type, num_children, confidence_range):
        self.assertEqual(node.label, label)
        self.assertEqual(node.node_type, node_type)
        self.assertEqual(len(node.children), num_children)
        self.assertEqual(node.confidence_range, confidence_range)
