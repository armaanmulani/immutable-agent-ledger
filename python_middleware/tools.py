import concurrent.futures
import datetime
import io
import platform
import sys
from ddgs import DDGS  # Clean import without deprecation warnings!
from schemas import ActionParameters


def execute_calculator(params: ActionParameters) -> str:
  """Executes basic arithmetic operations."""
  op, a, b = params.operation, params.a, params.b
  if a is None or b is None or not op:
    return "Error: Missing required parameters (a, b, operation)."

  try:
    if op == "add":
      return f"Result: {a + b}"
    elif op == "subtract":
      return f"Result: {a - b}"
    elif op == "multiply":
      return f"Result: {a * b}"
    elif op == "divide":
      return (
          "Error: Division by zero."
          if b == 0
          else f"Result: {a / b}"
      )
    else:
      return f"Error: Unsupported operation '{op}'."
  except Exception as e:
    return f"Error executing calculation: {str(e)}"


def execute_system_info(params: ActionParameters) -> str:
  """Returns basic system environment information."""
  current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  return (
      f"System OS: {platform.system()} {platform.release()} | Current Time:"
      f" {current_time}"
  )


def execute_python_interpreter(params: ActionParameters) -> str:
  """Executes arbitrary Python code dynamically and captures stdout output."""
  code = params.code
  if not code:
    return "Error: No 'code' parameter provided to execute."

  buffer = io.StringIO()
  sys.stdout = buffer

  try:
    exec_globals = {"__builtins__": __builtins__}
    exec_locals = {}

    exec(code, exec_globals, exec_locals)

    sys.stdout = sys.__stdout__
    output = buffer.getvalue().strip()

    if not output:
      output = (
          "Code executed successfully (No print output generated. Tip: Use"
          " print() to output results)."
      )

    return f"Code Execution Result:\n{output}"

  except Exception as e:
    sys.stdout = sys.__stdout__
    return f"Python Execution Error: {type(e).__name__} - {str(e)}"


def execute_web_search(params: ActionParameters) -> str:
  """Performs a web search using DDGS with a 5-second deadline."""
  query = params.query
  if not query:
    return "Error: No search 'query' parameter provided."

  def _search():
    with DDGS(timeout=5) as ddgs:
      return list(ddgs.text(query, max_results=3))

  try:
    with concurrent.futures.ThreadPoolExecutor() as executor:
      future = executor.submit(_search)
      results = future.result(timeout=5.0)

    if not results:
      return f"No search results found for query: '{query}'."

    formatted_results = []
    for idx, r in enumerate(results, 1):
      formatted_results.append(
          f"[{idx}] {r.get('title')}\nSnippet:"
          f" {r.get('body')}\nURL: {r.get('href')}"
      )

    return "\n\n".join(formatted_results)

  except concurrent.futures.TimeoutError:
    return "Web Search Error: Request timed out after 5 seconds."
  except Exception as e:
    return f"Web Search Error: {str(e)}"


def dispatch_action(action_name: str, params: ActionParameters) -> str:
  """Routes an action_name string to its corresponding Python function."""
  TOOL_MAP = {
      "calculator": execute_calculator,
      "system_info": execute_system_info,
      "python_interpreter": execute_python_interpreter,
      "web_search": execute_web_search,
  }

  tool_function = TOOL_MAP.get(action_name)
  if tool_function:
    return tool_function(params)
  else:
    return (
        f"Error: Unknown action '{action_name}'. Available tools:"
        f" {list(TOOL_MAP.keys())}"
    )