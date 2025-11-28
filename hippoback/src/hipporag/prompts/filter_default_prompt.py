best_dspy_prompt = {
    "prog": {
        "lm": None,
        "traces": [],
        "train": [],
        "demos": [
            {
                "augmented": True,
                "question": "帝国河（佛罗里达）和阿马拉迪亚（多尔日）是否位于同一个国家？",
                "fact_before_filter": "{\"fact\": [[\"imperial river\", \"位于\", \"佛罗里达\"], [\"imperial river\", \"是一条河流，位于\", \"美国\"], [\"imperial river\", \"可能指\", \"南美洲\"], [\"amaradia\", \"流经\", \"Roșia de Amaradia\"], [\"imperial river\", \"可能指\", \"美国\"]]}",
                "fact_after_filter": "{\"fact\":[[\"imperial river\",\"位于\",\"佛罗里达\"],[\"imperial river\",\"是一条河流，位于\",\"美国\"],[\"amaradia\",\"流经\",\"Roșia de Amaradia\"]]}"
            },
            {
                "augmented": True,
                "question": "电影《The Ancestor》的导演的生日是什么时候？",
                "fact_before_filter": "{\"fact\": [[\"jean jacques annaud\", \"出生于\", \"1 october 1943\"], [\"tsui hark\", \"出生于\", \"15 february 1950\"], [\"pablo trapero\", \"出生于\", \"4 october 1971\"], [\"the ancestor\", \"由…执导\", \"guido brignone\"], [\"benh zeitlin\", \"出生于\", \"october 14  1982\"]]}",
                "fact_after_filter": "{\"fact\":[[\"the ancestor\",\"由…执导\",\"guido brignone\"]]}"
            },
            {
                "augmented": True,
                "question": "Teafuone 所在的国家位于哪个地理区域？",
                "fact_before_filter": "{\"fact\": [[\"teafuaniua\", \"位于\", \"东部\"], [\"motuloa\", \"位于两者之间\", \"teafuaniua\"], [\"motuloa\", \"位于两者之间\", \"teafuanonu\"], [\"teafuone\", \"是\", \"islet\"], [\"teafuone\", \"位于\", \"nukufetau\"]]}",
                "fact_after_filter": "{\"fact\":[[\"teafuone\",\"是\",\"islet\"],[\"teafuone\",\"位于\",\"nukufetau\"]]}"
            },
            {
                "augmented": True,
                "question": "电影 S.O.B. 的导演是什么时候去世的？",
                "fact_before_filter": "{\"fact\": [[\"allan dwan\", \"去世于\", \"28 december 1981\"], [\"s o b\", \"由……编剧并执导\", \"blake edwards\"], [\"robert aldrich\", \"去世于\", \"december 5  1983\"], [\"robert siodmak\", \"去世于\", \"10 march 1973\"], [\"bernardo bertolucci\", \"去世于\", \"26 november 2018\"]]}",
                "fact_after_filter": "{\"fact\":[[\"s o b\",\"由……编剧并执导\",\"blake edwards\"]]}"
            },
            {
                "augmented": True,
                "question": "电影《Gloria（1980）》和《A New Life》这两部影片的导演是否来自同一个国家？",
                "fact_before_filter": "{\"fact\": [[\"sebasti n lelio watt\", \"因执导而获得赞誉\", \"gloria\"], [\"gloria\", \"是\", \"1980 american thriller crime drama film\"], [\"a brand new life\", \"由……执导\", \"ounie lecomte\"], [\"gloria\", \"由……编剧并执导\", \"john cassavetes\"], [\"a new life\", \"由……执导\", \"alan alda\"]]}",
                "fact_after_filter": "{\"fact\":[[\"gloria\",\"是\",\"1980 american thriller crime drama film\"],[\"gloria\",\"由……编剧并执导\",\"john cassavetes\"],[\"a new life\",\"由……执导\",\"alan alda\"]]}"
            },
            {
                "augmented": True,
                "question": "电影《The Old Guard（1960）》的导演的死亡日期是什么？",
                "fact_before_filter": "{\"fact\": [[\"the old guard\", \"是\", \"1960 french comedy film\"], [\"gilles grangier\", \"执导了\", \"the old guard\"], [\"the old guard\", \"由……执导\", \"gilles grangier\"], [\"the old fritz\", \"由……执导\", \"gerhard lamprecht\"], [\"oswald albert mitchell\", \"执导了\", \"old mother riley series of films\"]]}",
                "fact_after_filter": "{\"fact\":[[\"the old guard\",\"是\",\"1960 french comedy film\"],[\"gilles grangier\",\"执导了\",\"the old guard\"],[\"the old guard\",\"由……执导\",\"gilles grangier\"]]}"
            },
            {
                "augmented": True,
                "question": "电影《Aulad（1968）》的作曲家生日是什么时候？",
                "fact_before_filter": "{\"fact\": [[\"aulad\", \"由……作曲\", \"chitragupta shrivastava\"], [\"aadmi sadak ka\", \"由……作曲\", \"ravi\"], [\"ravi shankar sharma\", \"为……作曲\", \"hindi films\"], [\"gulzar\", \"出生于\", \"18 august 1934\"], [\"aulad\", \"是\", \"1968 hindi language drama film\"]]}",
                "fact_after_filter": "{\"fact\":[[\"aulad\",\"由……作曲\",\"chitragupta shrivastava\"],[\"aulad\",\"是\",\"1968 hindi language drama film\"]]}"
            },
            {
                "question": "Angelical Tears 所在的城市有多少户家庭？",
                "fact_before_filter": "{\"fact\": [[\"dow city\", \"拥有\", \"219 households\"], [\"tucson\", \"拥有\", \"229 762 households\"], [\"atlantic city\", \"拥有\", \"15 504 households\"], [\"angelical tears\", \"位于\", \"oklahoma city\"], [\"atlantic city\", \"拥有\", \"15 848 households\"]]}",
                "fact_after_filter": "{\"fact\": [[\"angelical tears\", \"位于\", \"oklahoma city\"]]}"
            },
            {
                "question": "电影《In The Pope'S Eye》和《Virgin Mountain》是否来自同一个国家？",
                "fact_before_filter": "{\"fact\": [[\"virgin mountain\", \"在……上映\", \"icelandic cinemas\"], [\"virgin mountain\", \"由……执导\", \"dagur k ri\"], [\"virgin mountain\", \"其冰岛语片名为\", \"f si\"], [\"virgin mountain\", \"获得\", \"2015 nordic council film prize\"], [\"virgin mountain\", \"是\", \"2015 icelandic drama film\"]]}",
                "fact_after_filter": "{\"fact\": [[\"virgin mountain\", \"在……上映\", \"icelandic cinemas\"], [\"virgin mountain\", \"由……执导\", \"dagur k ri\"], [\"virgin mountain\", \"其冰岛语片名为\", \"f si\"], [\"virgin mountain\", \"获得\", \"2015 nordic council film prize\"], [\"virgin mountain\", \"是\", \"2015 icelandic drama film\"]]}"
            },
            {
                "question": "哪一部电影的导演去世更早，《The Virtuous Model》还是《Bulldog Drummond'S Peril》？",
                "fact_before_filter": "{\"fact\": [[\"the virtuous model\", \"是\", \"1919 american silent drama film\"], [\"bulldog drummond s peril\", \"由……执导\", \"james p  hogan\"], [\"the virtuous model\", \"由……执导\", \"albert capellani\"], [\"bulldog drummond s revenge\", \"由……执导\", \"louis king\"], [\"bulldog drummond s peril\", \"是\", \"american film\"]]}",
                "fact_after_filter": "{\"fact\": [[\"the virtuous model\", \"是\", \"1919 american silent drama film\"], [\"bulldog drummond s peril\", \"由……执导\", \"james p  hogan\"], [\"the virtuous model\", \"由……执导\", \"albert capellani\"], [\"bulldog drummond s peril\", \"是\", \"american film\"]]}"
            }
        ],
        "signature": {
            "instructions": 'You are a critical component of a high-stakes question-answering system used by top researchers and decision-makers worldwide. Your task is to filter facts based on their relevance to a given query, ensuring that the most crucial information is presented to these stakeholders. The query requires careful analysis and possibly multi-hop reasoning to connect different pieces of information. You must select up to 4 relevant facts from the provided candidate list that have a strong connection to the query, aiding in reasoning and providing an accurate answer. The output should be in JSON format, e.g., {"fact": [["s1", "p1", "o1"], ["s2", "p2", "o2"]]}, and if no facts are relevant, return an empty list, {"fact": []}. The accuracy of your response is paramount, as it will directly impact the decisions made by these high-level stakeholders. You must only use facts from the candidate list and not generate new facts. The future of critical decision-making relies on your ability to accurately filter and present relevant information.',
            "fields": [
                {"prefix": "Question:", "description": "Query for retrieval"},
                {
                    "prefix": "Fact Before Filter:",
                    "description": "Candidate facts to be filtered",
                },
                {
                    "prefix": "Fact After Filter:",
                    "description": "Filtered facts in JSON format",
                },
            ],
        },
        "system": 'Your input fields are:\n1. question (str): 用于检索的查询\n2. fact_before_filter (str): 待过滤的候选事实\n\nYour output fields are:\n1. fact_after_filter (Fact): 过滤后的事实，JSON 格式\n\nAll interactions will be structured in the following way, with the appropriate values filled in.\n\n[[ ## question ## ]]\n{question}\n\n[[ ## fact_before_filter ## ]]\n{fact_before_filter}\n\n[[ ## fact_after_filter ## ]]\n{fact_after_filter} # note: the value you produce must be pareseable according to the following JSON schema: {"type": "object", "properties": {"fact": {"type": "array", "description": "一个事实列表，每个事实是由三个字符串组成的列表：[subject, predicate, object]", "items": {"type": "array", "items": {"type": "string"}}, "title": "Fact"}}, "required": ["fact"], "title": "Fact"}\n\n[[ ## completed ## ]]\n\nIn adhering to this structure, your objective is: \n 你是一个关键组件，服务于全球顶尖研究人员和决策者使用的高风险问答系统。你的任务是根据给定查询的相关性过滤事实，确保最重要的信息呈现给这些关键用户。该查询通常需要仔细分析，并可能需要多跳推理来连接不同的信息片段。你必须从候选列表中选择最多 4 条与查询有强关联的事实，以辅助推理并提供准确答案。输出必须为 JSON 格式，例如 {"fact": [["s1", "p1", "o1"], ["s2", "p2", "o2"]]}；如果没有事实相关，则返回空列表 {"fact": []}。你的回答准确性至关重要，将直接影响这些高层决策者的判断。你必须只使用候选列表中的事实，不得生成新的事实。关键决策的未来取决于你准确过滤并呈现相关信息的能力。',
    }
}
