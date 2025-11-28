import os
from src.hipporag.utils.config_utils import BaseConfig
from typing import List
import json
from src.hipporag import HippoRAG
from src.hipporag.utils.misc_utils import NewsRetrieved
from src.hipporag.utils.logging_utils import get_logger

logger = get_logger(__name__)

def get_hipporag(config: BaseConfig) -> HippoRAG:
    hipporag = HippoRAG(global_config=config)
    return hipporag


def index_docs(
    hipporag, news_file_path="/home/daisj/newsProj/test_data/data/news_sample.json"
) -> None:
    # TODO: 加载逻辑从数据库
    with open(news_file_path, "r") as f:
        news_data = json.load(f)
    logger.info(f"处理{len(news_data.keys())}条新闻数据")
    docs = []
    for i, (k, v) in enumerate(news_data.items()):
        news_passage = v["title"] + v["text"]
        # NOTE: doc 都是带有title+text 的 新闻
        docs.append(news_passage)

    hipporag.index(docs=docs)


def retrieve_queries(hipporag, queries: List[str]) -> List[NewsRetrieved | None]:

    res_QuerySolutionList = hipporag.retrieve(queries=queries)

    news_retrieved_list = [
        NewsRetrieved(
            question=item.question,
            passages=item.docs,  # QuerySolution.docs → passages
            passages_scores=item.doc_scores,
        )
        for item in res_QuerySolutionList
    ]

    return news_retrieved_list

def retrieve_query(hipporag, query: str) -> NewsRetrieved | None:
    return retrieve_queries(hipporag=hipporag, queries=[query])[0]

config = BaseConfig()
config.save_dir = "outputs/news_sample"  

rag = get_hipporag(config=config)
index_docs(rag)
news = retrieve_query(rag, "绿水青山怎么从沿海到内陆？")
print(news.passages[0:3])
print(news.passages_scores)
from src.hipporag.utils.misc_utils import compute_mdhash_id
news_ids = [compute_mdhash_id(text, prefix="chunk-") for text in news.passages]
for i in range(3):
    print(f"triples : {len(rag.map_docid_to_triples[news_ids[i]].triples)} ")
    print(rag.map_docid_to_triples[news_ids[i]])
    print(f"entities : {len(rag.map_docid_to_entities[news_ids[i]].unique_entities)} ")
    print(rag.map_docid_to_entities[news_ids[i]])

sub_graph_nodes = set()
for trple in rag.rerank_log['facts_after_rerank']:
    print(trple)
    
    sub_graph_nodes.add(trple[0])
    sub_graph_nodes.add(trple[2])
# 变成列表 
sub_graph_node_names =[compute_mdhash_id(node, prefix="entity-") for node in list(sub_graph_nodes)]

print("sub_graph_node_names:", sub_graph_node_names)

# 假设 graph 是 igraph Graph 对象
target_idx = []

for name in sub_graph_node_names:
    try:
        idx = rag.graph.vs.find(name=name).index
        target_idx.append(idx)
    except ValueError:
        print(f"节点 {name} 不存在于图中")


sub_graph = rag.graph.induced_subgraph(target_idx, implementation="create_from_scratch")

print(sub_graph.vs["name"])
for e in sub_graph.es:
    print(f"Edge {e.index}: {sub_graph.vs[e.source]['content']} -- {sub_graph.vs[e.target]['content']}, weight={e['weight']}")

# # standard_rag 检索测试
# from src.hipporag.StandardRAG import StandardRAG
# standard_rag = StandardRAG(global_config=config)
# with open("/home/daisj/newsProj/test_data/data/news_sample.json", "r") as f:
#         news_data = json.load(f)
# logger.info(f"处理{len(news_data.keys())}条新闻数据")
# docs = []
# for i, (k, v) in enumerate(news_data.items()):
#     news_passage = v["title"] + v["text"]
#     # NOTE: doc 都是带有title+text 的 新闻
#     docs.append(news_passage)
# standard_rag.index(docs=docs)
# news_standard = standard_rag.retrieve(queries=["绿水青山怎么从口号变成现实？"])
# print(news_standard[0].docs[0:3])