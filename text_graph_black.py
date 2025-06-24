import unittest
import random
from main import TextGraph

class TestGenerateNewText(unittest.TestCase):

    def setUp(self):
        # 固定随机种子，确保随机行为可复现
        random.seed(42)
        # 创建TextGraph实例并构建图（用固定文本）
        self.tg = TextGraph()
        sample_text = (
            "the scientist analyzed it again carefully analyzed the report"
        )
        # 直接构建图，避免文件IO
        words = self.tg.clean_text(sample_text).split()
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i + 1]
            self.tg.graph[w1][w2] += 1
            self.tg.directed_graph_nx.add_edge(w1, w2, weight=self.tg.graph[w1][w2])
    def test_EC1_all_bridge_words(self):
        # 输入所有两词之间都有桥接词的文本
        input_text = "the ANAlyzed, again"
        output = self.tg.generate_new_text(input_text)
        print("Test EC1 output:", output)
        # 期望结果中插入了桥接词 "scientist" 或 "it"（依图结构而定）
        self.assertIn("scientist", output.split() or "it" in output.split())
        self.assertTrue(output.startswith("the"))
        self.assertTrue(output.endswith("again"))

    def test_EC2_partial_bridge_words(self):
        input_text = "carefully analyzed again"
        output = self.tg.generate_new_text(input_text)
        print("Test EC2 output:", output)
        # 部分有桥接词，部分无
        self.assertTrue(output.startswith("carefully"))
        self.assertTrue(output.endswith("again"))
        # "it" 可能作为桥接词被插入
        self.assertIn("it", output.split() + [input_text.split()[1]])

    def test_EC3_no_bridge_words(self):
        input_text = "analyzed it again"
        output = self.tg.generate_new_text(input_text)
        print("Test EC3 output:", output)
        # 没有桥接词，输出应等于输入（忽略大小写）
        self.assertEqual(output, input_text.lower())

    def test_EC4_single_word(self):
        input_text = "team"
        output = self.tg.generate_new_text(input_text)
        print("Test EC4 output:", output)
        self.assertEqual(output, "team")

    def test_EC5_empty_string(self):
        input_text = ""
        output = self.tg.generate_new_text(input_text)
        print("Test EC5 output:", output)
        self.assertEqual(output, "")

if __name__ == "__main__":
    unittest.main()