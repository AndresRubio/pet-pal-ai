
import os

from llama_index.core import (
    load_index_from_storage,
    VectorStoreIndex,
    StorageContext,
)

from llama_index.vector_stores.faiss import FaissVectorStore
import faiss


def contains_excluded_words(url_to_check):
    excluded_words = ['exclusive', 'rodents', 'fish', 'top_brands', 'birds', 'aquarium', 'zooplus_exclusives']
    for word in excluded_words:
        if word in url_to_check:
            return True
    return False


def filter_paths(urls):
    # for url in urls:
    #     if url not in excluded_urls and not contains_excluded_words(url):
    #         urls.append(url)
    return [url for url in urls if not contains_excluded_words(url)]


def create_index(documents, wandb_callback, env='local') -> VectorStoreIndex:
    index = None
    if env == 'local':
        if os.path.exists("storage_faiss") and os.listdir("storage_faiss"):
            vector_store = FaissVectorStore.from_persist_dir("storage_faiss")
            storage_context = StorageContext.from_defaults(
                vector_store=vector_store, persist_dir="storage_faiss"
            )
            index = load_index_from_storage(storage_context=storage_context)
        else:
            faiss_index = faiss.IndexFlatL2(1536)
            storage_context = StorageContext.from_defaults(vector_store=FaissVectorStore(faiss_index=faiss_index))
            index = VectorStoreIndex.from_documents(
                documents,
                storage_context=storage_context,
                persist_dir="storage"
            )

            storage_context.persist(persist_dir='storage')
            wandb_callback.persist_index(index, index_name="aie-zooPalAI-index")
    elif env == 'wandb':
        #THERE IS SOME BUG WHEN TY TO LOAD THE INDEX FROM WANDB LOGIC USES DEFAULT FVALUE THAT DOES NOT EXIST
        storage_context = wandb_callback.load_storage_context(
            artifact_url=os.getenv("WANDB_INDEX_URL"), persist_dir="storage"
        )
        index = load_index_from_storage(storage_context)
    else:
        raise ValueError("Invalid environment")

    return index

