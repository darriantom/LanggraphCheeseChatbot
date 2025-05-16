import json

function_list = [
    {
        "type": "function",
        "function": {
            "name": "determine_sql_or_vector_or_nodb",
            "description": "This function is using conversation between user and assistant as input and determine whether using sql is good or using vectordb is good or it is good without db.",
            "parameters": {
                "type": "object",
                "properties": {
                    "which_db": {
                        "type": "string",
                        "enum": ["sql", "vector", "nodb"],
                        "description": "If using SQL is good this property returns 'sql', and if using vectordb is good return 'vector', and if information is not provided and it is a common dialogue like greetings, return 'nodb'"
                    }
                },
                "required": ["which_db"]
            }
        }
    }
]

sql_vector_tool = json.loads(json.dumps(function_list))