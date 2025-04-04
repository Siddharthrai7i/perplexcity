from typing import List
from sentence_transformers  import SentenceTransformer
import numpy as np

class SortSourceService:
    def __init__(self):
        self.embedding_model = SentenceTransformer("all-miniLM-L6-v2" , use_auth_token="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")

    def sort_sources(self , query:str ,search_results : List[dict]):
        relevant_docs=[]
        query_embedding = self.embedding_model.encode(query)
        print(query_embedding)

        for res in search_results:
            if not isinstance(res, dict):
                continue
            content = res.get("content")
            if content is None or not isinstance(content, str) or not content.strip():
                continue
            res_embedding = self.embedding_model.encode(res['content'])
            similarity=float(np.dot(query_embedding , res_embedding)/(np.linalg.norm(query_embedding)*np.linalg.norm(res_embedding)))
            
            # print(res_embedding)
            # print(similarity)

            res['relevance_score']=similarity

            if  similarity>0.3:
                relevant_docs.append(res)

        return sorted(relevant_docs , key =lambda x: x['relevance_score'] , reverse=True)     









