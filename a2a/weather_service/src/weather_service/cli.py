# Experiment to exercise weather_service graph
import sys, asyncio

from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage

from graph import get_graph, get_mcpclient

mcpclient = get_mcpclient() # A langchain_mcp_adapters.client.MultiServerMCPClient
# print(f"mcpclient is a {mcpclient}")

async def coromain():
    graph: StateGraph = await get_graph(mcpclient) # A langgraph.graph.state.CompiledStateGraph
    # print(f"graph is a {graph}")

    print(f"Enter text, control-D to exit")

    for line in sys.stdin:
        print(f"Hello, {line}")
        messages = [HumanMessage(content=line)]
        input = {"messages": messages}
        async for event in graph.astream(input, stream_mode="updates"):
            # events are dicts
            # print(f"Event is a {type(event)} with value {event}")
            # This loop coughs up three events, an 'assistant', a 'tools', and an 'assistant'
            # print(f"Event has keys {event.keys()}")
            if 'assistant' in event:
                assistant = event['assistant']
                if 'final_answer' in assistant:
                    print(f"Final answer: {assistant['final_answer']}")


loop = asyncio.get_event_loop()
loop.run_until_complete(coromain())  # run coromain() from sync code
pending = asyncio.Task.all_tasks()  # get all pending tasks
loop.run_until_complete(asyncio.gather(*pending))  # wait for tasks to finish normally
