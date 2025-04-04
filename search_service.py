from config import Settings 
from tavily import TavilyClient
import trafilatura


settings=Settings()
tavily_clint = TavilyClient(api_key=settings.SIDD_API_KEY)

class SearchService:
    def web_search(self , query:str):
       results=[]
       response=tavily_clint.search(query ,max_results=10 ) 
       search_result= response.get("results" , [])

       for result in search_result:
            downloaded=  trafilatura.fetch_url(result.get("url"))
            content = trafilatura.extract(downloaded , include_comments=False) 

            results.append(
                {
                        "titile":result.get("titile" ,""),
                        "url":result.get("url" ),
                        "content":content,
                }
            )

       return results

    