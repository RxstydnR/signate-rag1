from typing import List
from langchain_core.documents import Document

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
    # return "<chunk>"+"\n\n".join(doc.page_content for doc in docs) + "</chunk>"

def sort_sequential_chunks(docs):
    sorted_docs = sorted(docs, key=lambda x: x.metadata["position"])
    return sorted_docs

def group_continuous_positions(sorted_docs: List[Document]) -> List[List[Document]]:
    """
    ソート済みのDocumentオブジェクトのリストを連続したpositionごとにグループ化する
    """
    grouped_docs = []
    current_group = []
    expected_position = None

    for doc in sorted_docs:
        position = int(doc.metadata["position"])
        
        if expected_position is None or position == expected_position:
            current_group.append(doc)
        else:
            if current_group:
                grouped_docs.append(current_group)
            current_group = [doc]
        
        expected_position = position + 1
    
    # 最後のグループを追加
    if current_group:
        grouped_docs.append(current_group)
    
    return grouped_docs

def merge_sequential_chunks(chunks:List[str]) -> str:

    assert len(chunks)>0
    
    result = chunks[0]
    for chunk in chunks[1:]:
        # 重複部分を見つける
        overlap_end = 0
        for i in range(1, len(chunk) + 1):
            if result.endswith(chunk[:i]):
                overlap_end = i
        
        # 重複部分を除いて結合
        result += chunk[overlap_end:]
    
    return result


def merge_document_contents(grouped_docs: List[Document]):
    
    new_doc_list = []
    for group in grouped_docs:
        if len(group)>1:
            metadata = group[0].metadata
            page_contents = [doc.page_content for doc in group]
            merged_page_content = merge_sequential_chunks(page_contents)
            new_doc = Document(page_content=merged_page_content,metadata=metadata)
            new_doc_list.append(new_doc)
        else:
            new_doc_list.extend(group)
    return new_doc_list


from langchain.load import dumps, loads
def reciprocal_rank_fusion(results: list[list], k=60):
    """ reciprocal_rank_fusionは、ランク付けされた文書の複数のリストと、RRFの式で使われるオプションのパラメータkを受け取ります。 """
    
    # 各一意な文書の融合スコアを保持する辞書を初期化する
    fused_scores = {} # 各リストを繰り返し処理する

    # ランク付けされた文書のリストを繰り返し処理する
    for docs in results:
        # リスト内の各文書を、そのランク(リスト内の位置)で繰り返し処理する
        for rank, doc in enumerate(docs):
            # ドキュメントを文字列形式に変換してキーとして使用する (ドキュメントはJSONにシリアライズできると仮定)
            doc_str = dumps(doc)
            # ドキュメントがまだfused_scores辞書にない場合、初期スコアを0として追加する
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0
            # もしあれば、その文書の現在のスコアを取得する。
            previous_score = fused_scores[doc_str] # 文書の現在のスコアを取得する。
            # RRF の式を用いて文書のスコアを更新する： 1 / (rank + k)
            fused_scores[doc_str] += 1 / (rank + k)

    # 最終的な再ランク結果を得るために、融合されたスコアに基づいてドキュメントを降順にソートする
    reranked_results = [
        # (loads(doc), score)
        loads(doc)
        for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    ]

    # それぞれが文書とその融合スコアを含むタプルのリストとして、再ランクされた結果を返す
    return reranked_results


# def weighted_reciprocal_rank(self, doc_lists: List[List[Document]], weights = None, C=60) -> List[Document]:
#         """
#         Perform weighted Reciprocal Rank Fusion on multiple rank lists.
#         You can find more details about RRF here:
#         https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf

#         Args:
#             doc_lists: A list of rank lists, where each rank list contains unique items.

#         Returns:
#             list: The final aggregated list of items sorted by their weighted RRF
#                     scores in descending order.
#         """
#     if weights is None:
#         weights = [1]*len(doc_lists)
        
#     if len(doc_lists) != len(weights):
#         raise ValueError(
#             "Number of rank lists must be equal to the number of weights."
#         )

#     # Associate each doc's content with its RRF score for later sorting by it
#     # Duplicated contents across retrievers are collapsed & scored cumulatively
#     rrf_score: Dict[str, float] = defaultdict(float)
#     for doc_list, weight in zip(doc_lists, weights):
#         for rank, doc in enumerate(doc_list, start=1):
#             rrf_score[doc.page_content] += weight / (rank + C)

#     all_docs = chain.from_iterable(doc_lists)
#         sorted_docs = sorted(
#             unique_by_key(
#                 all_docs,
#                 lambda doc: doc.page_content,
#             ),
#             reverse=True,
#             key=lambda doc: rrf_score[doc.page_content],
#         )

#     # Docs are deduplicated by their contents then sorted by their scores
#     # all_docs = chain.from_iterable(doc_lists)
#     # sorted_docs = sorted(
#     #     unique_by_key(
#     #         all_docs,
#     #         lambda doc: doc.page_content,
#     #     ),
#     #     reverse=True,
#     #     key=lambda doc: rrf_score[
#     #         doc.page_content if self.id_key is None else doc.metadata[self.id_key]
#     #     ],
#     # )
#     return sorted_docs