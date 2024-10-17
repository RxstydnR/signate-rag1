<!-- <p align="center">-->
<img src="./figure/signate-rag1.png" alt="rag1">
<!-- </p> -->

# SIGNATE - RAG-1グランプリ \~みんなで生成AIの精度限界に挑戦！「ハルシネーション」の壁を越えよう！\~

## ソリューション
<img src="./figure/solution-overview.png" alt="solution">

## 最終結果
TBD

## メモ
- FAISS indexに格納しているチャンクには、multilingual-e5 largeを使う都合上、先頭にprefix「content: 」をつけている。このprefixをつけていないチャンクを持つBM25RetrieverとFAISSRetrieverをRRFする際に、チャンクの内容が一緒でもprefixの有無で異なるチャンクとみなされ、重複チャンクが除外されない。そのため、ほぼ同じチャンクをpromptに入れてしまっていた。現状のRRFのアルゴリズムはpage_contentをkeyに持つ辞書でスコアを管理しているため、チャンクの先頭のprefixを削除する処理を挟むか、それともmetadataに含めているチャンクのposition numberでRRFスコアを管理する仕様に変えるなどの対応が必要。
