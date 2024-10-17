from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate

# Data model
class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""
    datasource: Literal["retrieve", "count_string"] = Field(
        ...,
        description="Given a user question choose to route it to retrieve or count_string.",
    )

# Prompt
router_system_prompt = """あなたはユーザーの質問に対する回答に必要な情報収集を選択するエキスパートです。
情報収集の選択肢として「retrieve(検索)」「count_string(文字列カウント)」があります。
小説の内容を検索して回答できそうな質問の場合は「retrieve」、特定の文字列の出現回数をカウントする場合は「count_string」を選択してください。

# 例：
- 質問：「大学」という文字列が出てくる回数は？
- 方法：count_string

- 質問：登場人物の名前を全て挙げてください。
- 方法：retrieve

- 質問：ご飯を仲間と食べるシーンは何回か？
- 方法：retrieve
"""

router_human_prompt = """
# ユーザーの質問
- 質問：{question}
- 方法：
"""

router_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", router_system_prompt),
        ("human", router_human_prompt)
    ]
)
