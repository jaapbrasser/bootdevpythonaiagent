def call_function(function_call_part, verbose=False):
    from functions.get_files_info import get_files_info
    from functions.get_file_content import get_file_content
    from functions.run_python import run_python_file
    from functions.write_file import write_file

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    function_name = function_call_part.name
    args_dict = dict(function_call_part.args or {})
    args_dict["working_directory"] = "./calculator"

    if verbose:
        print(f"Calling function: {function_name}({args_dict})")
        
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in function_map:
        if verbose:
            print("⚠️  function_call_part.name is empty or None")
        return {
            "role": "tool",
            "parts": [
                {
                    "function_response": {
                        "name": function_name,
                        "response": {"error": f"Unknown function: {function_name}"}
                    }
                }
            ]
        }


    try:
        function_result = function_map[function_name](**args_dict)
        return {
            "role": "tool",
            "parts": [
                {
                    "function_response": {
                        "name": function_name,
                        "response": {"result": function_result}
                    }
                }
            ]
        }
    except Exception as e:
        return {
            "role": "tool",
            "parts": [
                {
                    "function_response": {
                        "name": function_name,
                        "response": {"error": str(e)}
                    }
                }
            ]
        }
