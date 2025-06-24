"""This module performs text-based graph analysis and visualization."""
import re
import random
import warnings

from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore", category=UserWarning,
                         message="No artists with labels found to put in legend.")
class TextGraph:
    """A class that builds and analyzes a directed graph from text."""
    def __init__(self):
        # 使用两个结构：一个自定义的嵌套dict图，一个networkx图用于可视化和高级算法
        self.graph = defaultdict(lambda: defaultdict(int))  # word1 -> {word2: count}
        self.directed_graph_nx = nx.DiGraph()  # 用于PageRank、可视化、最短路径等

    def clean_text(self, text):
        """Clean the input text by removing non-alphabetic 
        characters and converting to lowercase."""
        # 去除非字母字符，并转为小写
        return re.sub(r'[^A-Za-z\s]', ' ', text).lower()

    def build_graph(self, file_path):
        """This module performs text-based graph analysis and visualization."""
        # 从文本文件中读取内容并构建图结构
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        words = self.clean_text(text).split()
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i + 1]
            self.graph[w1][w2] += 1  # 统计边的权重
            self.directed_graph_nx.add_edge(w1, w2, weight=self.graph[w1][w2])  # 添加到networkx图

    def show_directed_graph(self):
        """This module performs text-based graph analysis and visualization."""
        # 打印邻接表并绘制图像
        print("Directed Graph (Adjacency List with weights):")
        for src, targets in self.graph.items():
            for tgt, wt in targets.items():
                print(f"{src} -> {tgt} [weight={wt}]")
        # 用matplotlib画图
        plt.figure(figsize=(12, 6))
        pos = nx.spring_layout(self.directed_graph_nx)
        nx.draw(self.directed_graph_nx, pos, with_labels=True,
                node_size=500, node_color="lightblue", arrows=True)
        labels = nx.get_edge_attributes(self.directed_graph_nx, 'weight')
        nx.draw_networkx_edge_labels(self.directed_graph_nx, pos, edge_labels=labels)
        plt.title("Directed Word Graph")
        plt.savefig("graph.png")
        plt.show()

    def query_bridge_words(self, word1, word2):
        """This module performs text-based graph analysis and visualization."""
        # 查询“桥接词”：即 word1 → ? → word2
        word1, word2 = word1.lower(), word2.lower()
        if word1 not in self.graph or word2 not in self.directed_graph_nx.nodes:
            return f"No {word1} or {word2} in the graph!"
        bridge_words = [mid for mid in self.graph[word1] if word2 in self.graph[mid]]
        if not bridge_words:
            return f"No bridge words from {word1} to {word2}!"
        return f"The bridge words from {word1} to {word2} are: {', '.join(bridge_words)}."

    def generate_new_text(self, input_text):
        """This module performs text-based graph analysis and visualization."""
        # 在两个单词之间插入桥接词（若存在）
        words = self.clean_text(input_text).split()
        new_words = []
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i + 1]
            new_words.append(w1)
            # 找桥接词
            bridges = [mid for mid in self.graph[w1] if w2 in self.graph[mid]]
            if bridges:
                new_words.append(random.choice(bridges))  # 随机选一个桥接词插入
        if words:
            new_words.append(words[-1])  # 添加最后一个词
        return ' '.join(new_words)
    #最短路径
    def calc_shortest_path(self, word1, word2=None):
        """Calculate and optionally visualize the
          shortest path(s) in the graph from word1 to word2."""
        word1 = word1.lower()
        if word1 not in self.directed_graph_nx:
            return f"{word1} not in graph!"

        if word2 is None:
            # 单词到所有节点的最短路径
            lengths, paths = nx.single_source_dijkstra(self.directed_graph_nx,
                                                    word1, weight='weight')
            for target in sorted(paths):
                if target == word1:
                    continue
                path_str = ' -> '.join(paths[target])
                print(f"{word1} -> {target}: {path_str} (length={lengths[target]})")
            return "All shortest paths from word1 shown above."

        word2 = word2.lower()
        if word2 not in self.directed_graph_nx:
            return f"{word2} not in graph!"

        try:
            paths = list(nx.all_shortest_paths(self.directed_graph_nx,
                                            word1, word2, weight='weight'))
            length = nx.dijkstra_path_length(self.directed_graph_nx, word1, word2, weight='weight')
            print(f"All shortest paths from {word1} to {word2} (length = {length}):")
            for p in paths:
                print(" -> ".join(p))

            self._visualize_paths(paths, word1, word2, length)
            return f"{len(paths)} shortest path(s) found of length {length}."

        except nx.NetworkXNoPath:
            return f"No path from {word1} to {word2}."


    def _visualize_paths(self, paths, word1, word2, length):
        """Helper function to visualize all shortest paths."""
        pos = nx.spring_layout(self.directed_graph_nx, seed=42)
        plt.figure(figsize=(12, 7))

        nx.draw_networkx(self.directed_graph_nx, pos, node_size=500,
                        node_color="lightblue", with_labels=True)
        edge_labels = nx.get_edge_attributes(self.directed_graph_nx, 'weight')
        nx.draw_networkx_edge_labels(self.directed_graph_nx, pos, edge_labels=edge_labels)

        color_map = plt.get_cmap("tab10", len(paths))
        for i, path in enumerate(paths):
            edges = list(zip(path, path[1:]))
            nx.draw_networkx_edges(
                self.directed_graph_nx,
                pos,
                edgelist=edges,
                edge_color=[color_map(i)],
                width=3,
                label=f'Path {i + 1}'
            )
            nx.draw_networkx_nodes(self.directed_graph_nx, pos,
                                nodelist=path, node_color=[color_map(i)], node_size=600)

        plt.title(f"All shortest paths from {word1} to {word2} (length = {length})")
        if paths:  # 有路径才显示图例
            plt.legend()
        plt.show()

    def cal_pagerank(self, word):
        """This module performs text-based graph analysis and visualization."""
        # 计算PageRank值
        pr = nx.pagerank(self.directed_graph_nx, alpha=0.85)
        return pr.get(word.lower(), 0.0)
    #随机游走
    def random_walk(self):
        """This module performs text-based graph analysis and visualization."""
        graph = self.directed_graph_nx
        if not graph:
            print("The graph is empty.")
            return

        current_node = random.choice(list(graph.nodes))
        print(f"Start from node: {current_node}")

        visited_edges = set()#已经拜访过的路径
        path = [current_node]

        while True:
            out_edges = list(graph.out_edges(current_node))
            if not out_edges:
                print(f"No outgoing edges from {current_node}. Walk ends.")
                break

            edge = random.choice(out_edges)
            if edge in visited_edges:
                print(f"Edge {edge} already visited. Walk ends.")
                break

            visited_edges.add(edge)
            _, next_node = edge
            path.append(next_node)

            print(f"Moved to: {next_node}")
            print(f"Current path: {' -> '.join(path)}")

            # 每次暂停时写入当前路径
            with open("random_walk_result.txt", "w", encoding="utf-8") as f:
                f.write(" -> ".join(path))

            user_input = input("Continue walking? (y/n): ").strip().lower()
            while user_input not in {'y', 'n'}:
                user_input = input("Please enter 'y' or 'n': ").strip().lower()
            if user_input == 'n':
                break
            current_node = next_node

        print("Random walk finished.")

def main():
    """This module performs text-based graph analysis and visualization."""
    tg = TextGraph()
    file_path = input("Enter path to text file: ")
    tg.build_graph(file_path)

    # 命令行交互菜单
    while True:
        print("\nMenu:")
        print("1. Show Directed Graph")
        print("2. Query Bridge Words")
        print("3. Generate New Text with Bridge Words")
        print("4. Calculate Shortest Path")
        print("5. Calculate PageRank")
        print("6. Random Walk")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            tg.show_directed_graph()
        elif choice == '2':
            w1 = input("Enter first word: ")
            w2 = input("Enter second word: ")
            print(tg.query_bridge_words(w1, w2))
        elif choice == '3':
            line = input("Enter a new line of text: ")
            print(tg.generate_new_text(line))
        elif choice == '4':
            input_line = input("Enter source and optional " \
            "destination word (1 or 2 words): ").strip().split()
            if len(input_line) == 1:
                w1 = input_line[0]
                print(tg.calc_shortest_path(w1))
            elif len(input_line) == 2:
                w1, w2 = input_line
                print(tg.calc_shortest_path(w1, w2))
            else:
                print("Please enter one or two words only.")
        elif choice == '5':
            word = input("Enter word to calculate PageRank: ")
            print(f"PageRank of '{word}' is {tg.cal_pagerank(word):.4f}")
        elif choice == '6':
            print("Random walk result:")
            print(tg.random_walk())
        elif choice == '7':
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
