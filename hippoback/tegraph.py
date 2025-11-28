import pickle
import igraph as ig


with open("/home/daisj/newsProj/HippoRAG-d/outputs/newstest/qwen3-vl-235b-a22b-instruct_qwen3-embedding-8b/graph.pickle", "rb") as f:
    graph: ig.Graph = pickle.load(f)

print(graph.summary())

# for v in graph.vs:
#     print(v.index, v["content"][:50])

# for e in graph.es:
#     print(e.index, graph.vs[e.source]["content"][:50], "===" ,graph.vs[e.target]["content"][:50], e["weight"])


# 加载 parquet 文件内容
import pandas as pd
df = pd.read_parquet("/home/daisj/newsProj/HippoRAG-d/outputs/newstest/qwen3-vl-235b-a22b-instruct_qwen3-embedding-8b/fact_embeddings/vdb_fact.parquet")
print(df)

import igraph as ig

g = ig.Graph(directed=False)
g.add_vertices(2)

# 两条重复边 weight=1
g.add_edges([(0,1),(0,1)], attributes={"weight":[1,1]})
print("Before simplify:", g.es["weight"])  # [1, 1]

#  单独打印每条边
for e in g.es:
    print(f"Edge {e.index}: {e.source} -- {e.target}, weight={e['weight']}")

g.simplify(combine_edges={"weight":"sum"})
print("After simplify:", g.es["weight"])   # [2]

#  单独打印每条边
for e in g.es:
    print(f"Edge {e.index}: {e.source} -- {e.target}, weight={e['weight']}")