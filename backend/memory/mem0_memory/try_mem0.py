import os
from mem0 import Memory

os.environ["GROQ_API_KEY"] = "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"

config = {
    "llm": {
        "provider": "groq",
        "config": {
            "model": "llama-3.3-70b-versatile",
            "temperature": 0.1,
            "max_tokens": 1000,
        }
    }
}

mem0 = Memory.from_config(config)

# 1. Add: Store a memory from any unstructured text
result = mem0.add("I am working on improving my tennis skills. Suggest some online courses.", user_id="alice", metadata={"category": "hobbies"})

# Created memory --> 'Improving her tennis skills.' and 'Looking for online suggestions.'
print(result)

# 2. Query: Retrieve memories based on a query
result = mem0.search("what was the game i searched for last time?", user_id="alice")

# Retrieved memories --> 'Improving her tennis skills.' and 'Looking for online suggestions.'
print("***************RESULT****************")
print(result)
