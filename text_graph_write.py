import unittest
from main import TextGraph

class test_query_bridge_words(unittest.TestCase):
    def setUp(self):
        self.tg = TextGraph()
        sample_text = (
            "carefully analyzed the report. "
            "the report was wrote and shared by the scientist."
        )
        with open("sample.txt", "w", encoding="utf-8") as f:
            f.write(sample_text)
        self.tg.build_graph("sample.txt")
    # 输入 word1=hello, word2=the，第一个词不在图中
    def test_TC1(self):
        result = self.tg.query_bridge_words("hello", "the")
        print(f"TC1 actual output: {result}")
        self.assertEqual(result, "No hello or the in the graph!")
    # 输入 word1=the, word2=hello，第二个词不在图中
    def test_TC2(self):
        result = self.tg.query_bridge_words("the", "hello")
        print(f"TC2 actual output: {result}")
        self.assertEqual(result, "No the or hello in the graph!")
    # 输入 word1=the, word2=carefully，有词但无桥接词(3)
    def test_TC3(self):
        result = self.tg.query_bridge_words("the", "carefully")
        print(f"TC3 actual output: {result}")
        self.assertEqual(result, "No bridge words from the to carefully!")
    # 输入 word1=carefully, word2=the，有桥接词 analyzed(4)
    def test_TC4(self):
        result = self.tg.query_bridge_words("carefully", "the")
        print(f"TC4 actual output: {result}")
        self.assertEqual(result, "The bridge words from carefully to the are: analyzed.")
if __name__ == '__main__':
    unittest.main(verbosity=2)