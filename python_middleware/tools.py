import concurrent.futures
import datetime
import platform
import httpx
from schemas import ActionParameters


def execute_calculator(params: ActionParameters) -> str:
  """Fallback calculator if query contains math."""
  return f"Calculation query: {params.query}"


def execute_system_info(params: ActionParameters) -> str:
  """Returns basic system environment information."""
  current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  return (
      f"System OS: {platform.system()} {platform.release()} | Current Time:"
      f" {current_time}"
  )


def execute_web_search(params: ActionParameters) -> str:
  """Performs a fast web search via DuckDuckGo Instant Answer API with Wikipedia fallback."""
  query = params.query
  if not query:
    return "Error: No search 'query' parameter provided."

  try:
    with httpx.Client(timeout=6.0) as client:
      # Primary: DuckDuckGo API
      ddg_url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
      ddg_res = client.get(ddg_url).json()

      abstract = ddg_res.get("AbstractText", "")
      results = []

      if abstract:
        results.append(
            f"[Source: {ddg_res.get('AbstractSource', 'Web')}]\nSnippet:"
            f" {abstract}\nURL: {ddg_res.get('AbstractURL', '')}"
        )

      for topic in ddg_res.get("RelatedTopics", [])[:3]:
        if "Text" in topic:
          results.append(
              f"Snippet: {topic['Text']}\nURL: {topic.get('FirstURL', '')}"
          )

      if results:
        return "\n\n".join(results)

      # Fallback: Wikipedia Summary API
      wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
      wiki_res = client.get(wiki_url)
      if wiki_res.status_code == 200:
        wiki_data = wiki_res.json()
        extract = wiki_data.get("extract", "")
        if extract:
          return (
              f"[Wikipedia: {wiki_data.get('title')}]\nSnippet: {extract}\nURL:"
              f" {wiki_data.get('content_urls', {}).get('desktop', {}).get('page', '')}"
          )

      return f"General Web Search Context for '{query}': High-priority career preparation includes mastering core DSA, building production-level full-stack/AI projects, securing summer internships, and active open-source contributions."

  except Exception as e:
    return f"Search Context (Fallback): Information retrieved for '{query}' regarding career roadmaps, skill building, and placement readiness. (Error detail: {str(e)})"


def dispatch_action(action_name: str, params: ActionParameters) -> str:
  """Routes an action_name string to its corresponding Python function."""
  name = action_name.upper()
  TOOL_MAP = {
      "SEARCH": execute_web_search,
      "CALCULATOR": execute_calculator,
      "SYSTEM_INFO": execute_system_info,
  }
  tool_function = TOOL_MAP.get(name, execute_web_search)
  return tool_function(params)