from mcp.types import CallToolResult, TextContent
from mcp.server.fastmcp import FastMCP, Context
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import (
    DuckDuckGoSearchException,
    RatelimitException,
    TimeoutException,
)


def format_result_for_llm(result: dict[str, str]) -> str:
    """Format result in a natural language style that's easier for LLMs to process"""
    return (
        f"Title: {result['title']}\nLink: {result['href']}\nContent: {result['body']}"
    )


def format_results_for_llm(results: list[dict[str, str]]) -> str:
    """Format results in a natural language style that's easier for LLMs to process"""
    if not results or len(results) == 0:
        return "No search results found."

    formatted_results = []
    for result in results:
        formatted_results.append(format_result_for_llm(result))

    return "\n\n".join(formatted_results)


# Initialize FastMCP server
mcp = FastMCP("duckduckgo")


@mcp.tool()
async def search(
    query: str, ctx: Context, max_results: int = 10
) -> list[dict[str, str]]:
    """
    Web Search Tool using DuckDuckGo and returning formatted results.

    Args:
        query: The search query string
        max_results: Maximum number of results to return (default: 10)
        ctx: MCP context for logging
    """
    try:
        ctx.info(f"Searching for '{query}' with max_results={max_results}...")
        results = DDGS().text(query, max_results=max_results)
        if not results or len(results) == 0:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text", text=f"No search results found for '{query}'."
                    )
                ]
            )

        return CallToolResult(
            content=[
                TextContent(type="text", text=format_result_for_llm(result))
                for result in results
            ]
        )
    except DuckDuckGoSearchException as e:
        await ctx.error(f"DuckDuckGo search failed: {str(e)}")
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Failed to retrieve results from DuckDuckGo: {str(e)}",
                )
            ],
            isError=True,
        )
    except RatelimitException as e:
        await ctx.error(f"Rate limit exceeded: {str(e)}")
        return CallToolResult(
            content=[
                TextContent(
                    type="text", text="Rate limit exceeded. Please try again later."
                )
            ],
            isError=True,
        )
    except TimeoutException as e:
        await ctx.error(f"Search request timed out: {str(e)}")
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text="Search request timed out. Please try again later.",
                )
            ],
            isError=True,
        )
    except Exception as e:
        await ctx.error(f"Search request timed out: {str(e)}")
        return CallToolResult(
            content=[
                TextContent(
                    type="text", text=f"An error occurred while searching: {str(e)}"
                )
            ],
            isError=True,
        )


def run():
    # Initialize and run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    run()
