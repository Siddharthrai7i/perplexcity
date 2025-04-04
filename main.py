from fastapi import FastAPI , WebSocket 
import asyncio

from chat_body import ChatBody
from search_service import SearchService
from sort_source_service import SortSourceService
from llm_service import LLMService



app=FastAPI()
search_service=SearchService()
sort_source_service=SortSourceService()
llm_service=LLMService()

@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket:WebSocket):
    await websocket.accept()

    try:
        await asyncio.sleep(0.1)
        data=await websocket.receive_json()
        query=data.get("query")

        search_results=search_service.web_search(query)
        sorted_results=sort_source_service.sort_sources(query , search_results)
        await websocket.send_json({"type":"search_results" ,"data": sorted_results})

        for chunk in llm_service.generate_response(query , sorted_results):
            await asyncio.sleep(0.1)
            await websocket.send_json({"type":"content" , "data":chunk}) 
    except:
        print("Unexpected error occoured ")
    finally:
        await websocket.close()



@app.post("/chat")
def chat_endpoint(body: ChatBody):
    search_results=search_service.web_search(body.query)
    sorted_results=sort_source_service.sort_sources(body.query , search_results)
    response =llm_service.generate_response(body.query , sorted_results)
    return response 





