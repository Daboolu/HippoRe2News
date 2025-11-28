from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import igraph as ig
import json
from src.hipporag.utils.config_utils import BaseConfig
from src.hipporag import HippoRAG
from src.hipporag.utils.misc_utils import compute_mdhash_id

from fastapi.middleware.cors import CORSMiddleware

class QueryRequest(BaseModel):
    query: str


class NewsRetrieved(BaseModel):
    question: str
    passages: List[str]
    passages_scores: List[float]
    passages_mdhash: List[str]

# ==================== 全局缓存 ====================
global_graph = None
global_doc_triple_map = None
global_last_res = None


# ==================== Pydantic models ====================
class QueryRequest(BaseModel):
    query: str

class ExpandRequest(BaseModel):
    current_nodes: List[str]

class EdgeInfo(BaseModel):
    source: str
    target: str
    relation: str
    weight: float

class GraphResponse(BaseModel):
    query: str
    triples: List[List[str]]
    entities: List[str]
    subgraph_nodes: List[str]
    subgraph_edges: List[EdgeInfo]
    passages: List[str]
    passages_scores: List[float]
    passages_mdhash: List[str]



app = FastAPI(title="HippoRAG News Retrieval API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本地开发阶段允许全部来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_hipporag(config: BaseConfig) -> HippoRAG:
    return HippoRAG(global_config=config)


def index_docs(hipporag, news_file_path="/home/daisj/newsProj/test_data/data/news_sample.json"):
    with open(news_file_path, "r") as f:
        news_data = json.load(f)
    docs = [v["title"] + v["text"] for _, v in news_data.items()]
    hipporag.index(docs=docs)


config = BaseConfig()
config.save_dir = "outputs/news_sample"

rag = get_hipporag(config)
index_docs(rag)

@app.post("/retrieve", response_model=NewsRetrieved)
def retrieve(req: QueryRequest):
    res = rag.retrieve(queries=[req.query])[0]
    return NewsRetrieved(
        question=req.query,
        passages=res.docs,
        passages_scores=res.doc_scores,
        passages_mdhash=[compute_mdhash_id(x) for x in res.docs],
    )

# ==================== API1: 初次检索与构图 ====================
@app.post("/graph/subgraph_all", response_model=GraphResponse)
def graph_subgraph_all(req: QueryRequest):
    global global_graph, global_doc_triple_map, global_last_res

    # 1) retrieve
    res = rag.retrieve(queries=[req.query])[0]
    news_ids = [compute_mdhash_id(text, prefix="chunk-") for text in res.docs]

    # 2) collect triples
    all_triples = []
    doc_triple_map = {}
    for nid in news_ids:
        triples_obj = rag.map_docid_to_triples.get(nid)
        if triples_obj:
            all_triples.extend(triples_obj.triples)
            doc_triple_map[nid] = triples_obj.triples

    # 3) build full graph
    graph_all_triples = ig.Graph(directed=False)
    node_index = {}
    next_idx = 0

    def get_node_idx(entity):
        nonlocal next_idx
        if entity not in node_index:
            graph_all_triples.add_vertices(1)
            graph_all_triples.vs[next_idx]["name"] = compute_mdhash_id(entity, prefix="entity-")
            graph_all_triples.vs[next_idx]["content"] = entity
            node_index[entity] = next_idx
            next_idx += 1
        return node_index[entity]

    # build edges
    for h, r, t in all_triples:
        h_i = get_node_idx(h)
        t_i = get_node_idx(t)

        graph_all_triples.add_edges([(h_i, t_i)])
        e_idx = graph_all_triples.ecount() - 1

        h_md = compute_mdhash_id(h, prefix="entity-")
        t_md = compute_mdhash_id(t, prefix="entity-")

        try:
            src = rag.graph.vs.find(name=h_md).index
            tgt = rag.graph.vs.find(name=t_md).index
            oe = rag.graph.get_eid(src, tgt, directed=False, error=False)
            weight = rag.graph.es[oe]["weight"] if oe != -1 else 1.0
        except ValueError:
            weight = 1.0

        graph_all_triples.es[e_idx]["weight"] = weight
        graph_all_triples.es[e_idx]["relation"] = r

    # 4) initial subgraph via rerank
    sub_nodes_real = set()
    for h, r, t in rag.rerank_log["facts_after_rerank"]:
        sub_nodes_real.add(h)
        sub_nodes_real.add(t)

    target_idx = []
    for e in sub_nodes_real:
        try:
            idx = graph_all_triples.vs.find(content=e).index
            target_idx.append(idx)
        except ValueError:
            pass

    sub_graph = graph_all_triples.induced_subgraph(target_idx, implementation="create_from_scratch")

    # 5) find contributing passages
    contributing_docs = []
    sub_entities = set(sub_graph.vs["content"])

    for docid, triples in doc_triple_map.items():
        for h, r, t in triples:
            if h in sub_entities or t in sub_entities:
                contributing_docs.append(docid)
                break

    related_passages = []
    related_scores = []
    related_mdhash = []

    for i, d in enumerate(res.docs):
        md = compute_mdhash_id(d, prefix="chunk-")
        if md in contributing_docs:
            related_passages.append(d)
            related_scores.append(res.doc_scores[i])
            related_mdhash.append(md)

    # edges
    subgraph_edges = []
    for e in sub_graph.es:
        subgraph_edges.append(
            EdgeInfo(
                source=sub_graph.vs[e.source]["content"],
                target=sub_graph.vs[e.target]["content"],
                relation=e["relation"],
                weight=e["weight"],
            )
        )

    # cache globals
    global_graph = graph_all_triples
    global_doc_triple_map = doc_triple_map
    global_last_res = res

    return GraphResponse(
        query=req.query,
        triples=all_triples,
        entities=list(node_index.keys()),  # 实体文本
        subgraph_nodes=sub_graph.vs["content"],  # 实体文本
        subgraph_edges=subgraph_edges,
        passages=related_passages,
        passages_scores=related_scores,
        passages_mdhash=related_mdhash,
    )



# ==================== API2: 扩展一跳 ====================
@app.post("/graph/subgraph_expand", response_model=GraphResponse)
def graph_subgraph_expand(req: ExpandRequest):
    global global_graph, global_doc_triple_map, global_last_res

    graph_all_triples = global_graph
    doc_triple_map = global_doc_triple_map
    res = global_last_res

    original_nodes = set(req.current_nodes)
    neighbor_idx = set()
    expanded_idx = set()

    # core fix: find by "content" not "name"
    for ent in original_nodes:
        try:
            v = graph_all_triples.vs.find(content=ent)
        except ValueError:
            continue

        expanded_idx.add(v.index)
        for nb in graph_all_triples.neighbors(v.index):
            neighbor_idx.add(nb)
            # break

    expanded_idx.update(neighbor_idx)

    if not expanded_idx:
        sub_graph = graph_all_triples.induced_subgraph([], implementation="create_from_scratch")
    else:
        sub_graph = graph_all_triples.induced_subgraph(list(expanded_idx), implementation="create_from_scratch")

    # contributing docs
    sub_entities = set(sub_graph.vs["content"])
    contributing_docs = []

    for docid, triples in doc_triple_map.items():
        for h, r, t in triples:
            if h in sub_entities or t in sub_entities:
                contributing_docs.append(docid)
                break

    related_passages = []
    related_scores = []
    related_mdhash = []
    for i, d in enumerate(res.docs):
        md = compute_mdhash_id(d, prefix="chunk-")
        if md in contributing_docs:
            related_passages.append(d)
            related_scores.append(res.doc_scores[i])
            related_mdhash.append(md)

    subgraph_edges = []
    for e in sub_graph.es:
        subgraph_edges.append(
            EdgeInfo(
                source=sub_graph.vs[e.source]["content"],
                target=sub_graph.vs[e.target]["content"],
                relation=e["relation"],
                weight=e["weight"],
            )
        )

    return GraphResponse(
        query="expand",
        triples=[],
        entities=sub_graph.vs["content"],
        subgraph_nodes=sub_graph.vs["content"],
        subgraph_edges=subgraph_edges,
        passages=related_passages,
        passages_scores=related_scores,
        passages_mdhash=related_mdhash,
    )



from src.hipporag.StandardRAG import StandardRAG

standard_rag = StandardRAG(global_config=config)
index_docs(standard_rag)

@app.post("/standard/retrieve", response_model=NewsRetrieved)
def retrieve_standard(req: QueryRequest):
    res = standard_rag.retrieve(queries=[req.query])[0]
    return NewsRetrieved(
        question=req.query,
        passages=res.docs,
        passages_scores=res.doc_scores if hasattr(res, "doc_scores") else [],
        passages_mdhash=[compute_mdhash_id(x) for x in res.docs],
    )

