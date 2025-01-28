import json
import requests
from abc import ABC, abstractmethod


from backend.utils.json_utils import pre_process_the_json_response, load_object_from_string
from backend.llms.groq_llm.inference import GroqInference

SERPER_API_KEY = ""
llm = GroqInference()


SYSTEM_PROMPT = """
You are an expert in searching through the web and providing information after analysing the search results you get. 
You will be given a user query using which you should analyse and create appropriate search queries.

The tools which you have access to are:
1. browsertool: This is a tool to browse the web
   parameters:
   - query: The query to search for
2. finishtool: This tool should be called when you have found the information you need. 
   parameters:
   - summary: The summary of the information you have found
   
Always use the finishtool to finish the task.

Response in JSON format.
```json
{
  "reasoning": "Generate the reasoning/ thought process you went through to choose the tool and parameters",
  "tool_name": "browsertool",
  "parameters": {
    Use the parameters as per the tool
  }
}
```

Notes:
    1. Only generate one tool call at a time.
    2. Do not generate multiple tool calls.
    3. Only response in JSON format.
    
"""

class BrowserAgent:
    def __init__(self):
        pass

    def run(self, query):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"User query: {query}"},
        ]
        response = None
        
        while True:
            print("\n=== Generating LLM Response ===")
            response = llm.generate_response(messages=messages)
            messages.append({"role": "assistant", "content": response})
            
            parsed_response = pre_process_the_json_response(response)
            response_object = load_object_from_string(parsed_response)
            
            print("\n=== Agent Response ===")
            print(f"Reasoning: {response_object.get('reasoning')}")
            print(f"Tool: {response_object.get('tool_name')}")
            print(f"Parameters: {json.dumps(response_object.get('parameters'), indent=2)}")
            
            print("\n=== Running Tool ===")
            continue_flag, response = self._run_tool(response_object.get("tool_name"), response_object.get("parameters"))
            
            if continue_flag:
                print("\n=== Tool Output ===")
                print(response)
                messages.append({"role": "user", "content": f"Observations: {response}"})
            else:
                print("\n=== Final Response ===")
                print(response)
                return response
        
        return response
            
            
            

    def _run_tool(self, tool_name, tool_input):
        if tool_name == "browsertool":
            tool = BrowserTool()
            response = tool.execute(tool_input)
            return True, response   
        elif tool_name == "finishtool":
            response = tool_input.get("summary")
            return False, response


class Tool:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, input):
        pass


class BrowserTool(Tool):
    def __init__(self):
        super().__init__("browsertool", "This is a tool to browse the web")

    def execute(self, input):
        results = self.search(input.get("query"))
        return self.get_snippets_from_search_results(results)

    def search(self, query):
        """Do a search on the web

        Args:
            query (str): The query to search for
        """
        url = "https://google.serper.dev/search"
        payload = json.dumps(
            {
                "q": query,
            }
        )
        headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

    def get_snippets_from_search_results(self, results):
        """Parse the search results

        Args:
            results (dict): The search results
        """
        organic_answers = results.get("organic", [])
        snippets = [answer.get("snippet", "") for answer in organic_answers]
        return "\n".join(snippets)

    def summarize_snippets(self, snippets: str) -> str:
        """Summarize the snippets

        Args:
            snippets (str): The snippets to summarize
        """
        
        # TODO: Use the LLM to summarize the snippets
        system_prompt = """
        You are a summarizer. You are given a list of snippets and you need to summarize them.
        """
        user_prompt = f"Here are the snippets: {snippets}"
        
        return llm.generate_response(messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}])

if __name__ == "__main__":
    agent = BrowserAgent()
    agent.run("Give me some information about places to visit in Bengaluru")
