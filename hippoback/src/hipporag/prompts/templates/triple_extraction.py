from .ner import one_shot_ner_paragraph, one_shot_ner_output
from ...utils.llm_utils import convert_format_to_template

ner_conditioned_re_system = """
你的任务是根据给定的新闻段落以及其核心实体列表，抽取对应的 RDF（三元组）关系图谱，并以 JSON 格式返回。

【目标】
从新闻文本中识别出最重要的事件关系，并以三元组 (主语, 谓语, 宾语) 的形式输出，用于构建新闻脉络图谱。

【严格要求】
1. 三元组中的主语与宾语必须优先来自核心实体列表。
2. 若文本中出现代词（如“他”“她”“其方”“中方”“日方”等），必须解析并替换成对应的实体名称。
3. 三元组必须代表新闻事实，不要推理或补全未出现的信息。

【输出格式】
{
    "triples": [
        ["主语", "谓语", "宾语"],
        ...
    ]
}

请基于上述要求，从新闻段落中抽取高质量关系三元组。
"""




ner_conditioned_re_frame = """
注意:
根据提供给你的命名的实体从原文中捕捉关系,关注 **人物与人物** 、 **人物与地点**、 **人物与事件** 、**国家与人物**、**人物与议题** 之间的关系。

新闻段落:
```
{passage}
```

{named_entity_json}
"""


ner_conditioned_re_input = ner_conditioned_re_frame.format(
    passage=one_shot_ner_paragraph, named_entity_json=one_shot_ner_output
)


ner_conditioned_re_output = """{"triples": [
    ["李强", "会见", "佐科·维多多"],
    ["李强", "出席", "东盟峰会"],
    ["李强", "出席于", "雅加达"],
    ["中国国务院总理", "是", "李强"],
    ["印尼总统", "是", "佐科·维多多"],
    ["佐科·维多多", "会见地点", "雅加达"],
    ["李强", "讨论议题", "一带一路"],
    ["李强", "讨论议题", "雅万高铁"],
    ["佐科·维多多", "讨论议题", "一带一路"],
    ["雅万高铁", "位于", "印尼"],
    ["中国", "参与合作", "一带一路"],
    ["印度尼西亚", "参与合作", "一带一路"],
    ["中国", "双边合作包括", "雅万高铁"]
]

}
"""

prompt_template = [
    {"role": "system", "content": ner_conditioned_re_system},
    {"role": "user", "content": ner_conditioned_re_input},
    {"role": "assistant", "content": ner_conditioned_re_output},
    {
        "role": "user",
        "content": convert_format_to_template(
            original_string=ner_conditioned_re_frame,
            placeholder_mapping=None,
            static_values=None,
        ),
    },
]
