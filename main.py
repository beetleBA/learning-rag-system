# from chunkers.chunking import chunk_document
# from loaders.pipeline import process_pdf
#
# from embeddings.encoder import TextEmbedder
# from storage.qdrant import QdrantStorage
#
#
# # 1. Извлекаем текст из PDF
# document = process_pdf("examples/1.pdf")
#
# # 2. Разбиваем документ на чанки
# chunks = chunk_document(document)
#
# print(f"Всего чанков: {len(chunks)}")
#
# # 3. Создаём векторы
# embedder = TextEmbedder()
# vectors = embedder.embed_chunks(chunks)
#
# print(f"Создано векторов: {len(vectors)}")
#
# # 4. Подключаемся к Qdrant
# storage = QdrantStorage()
#
# try:
#     # 5. Создаём коллекцию
#     storage.create_collection()
#
#     # 6. Сохраняем чанки и векторы
#     storage.save_chunks(chunks, vectors)
#
#     # 7. Проверяем результат
#     count = storage.count_points()
#
#     print(f"Точек в Qdrant: {count}")
#
# finally:
#     storage.close()



# from embeddings.encoder import TextEmbedder
# from storage.qdrant import QdrantStorage
#
#
# embedder = TextEmbedder()
# storage = QdrantStorage()
#
# try:
#     query = "С какого символа начинается переменная в PHP?"
#
#     # Преобразуем вопрос в вектор
#     query_vector = embedder.embed_query(query)
#
#     # Ищем похожие чанки
#     results = storage.search(
#         query_vector=query_vector,
#         limit=3,
#     )
#
#     print(f"Вопрос: {query}")
#     print(f"Найдено результатов: {len(results)}")
#
#     for result in results:
#         print("\n" + "=" * 50)
#         print(f"Страница: {result['page_number']}")
#         print(f"Чанк: {result['chunk_index']}")
#         print(f"Оценка сходства: {result['score']:.4f}")
#         print(f"Текст:\n{result['text']}")
#
# finally:
#     storage.close()



#
# from embeddings.encoder import TextEmbedder
# from storage.qdrant import QdrantStorage
#
# from generation.gigachat_client import GigaChatGenerator
# from generation.service import RAGService
#
# import json
#
#
# embedder = TextEmbedder()
# storage = QdrantStorage()
# generator = GigaChatGenerator()
#
# try:
#     rag = RAGService(
#         embedder=embedder,
#         storage=storage,
#         generator=generator,
#     )
#
#     question = "Кто должен быть госпитализированы в стационар?"
#
#     response = rag.answer(
#         question=question,
#         top_k=3,
#     )
#
#     print("\n=== RAG RESPONSE ===")
#
#     print(
#         json.dumps(
#             response,
#             ensure_ascii=False,
#             indent=4,
#         )
#     )
#
# finally:
#     storage.close()
