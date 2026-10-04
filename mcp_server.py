
from mcp.server.fastmcp import FastMCP
import curriculum_data

mcp = FastMCP("csc51-curriculum")


@mcp.tool()
def get_week_topics(week: int) -> str:
    data = curriculum_data.get_week_data(week)

    return (
        f"Period 1: {data['period_1']}\n"
        f"Period 2: {data['period_2']}"
    )


@mcp.tool()
def get_performance_criteria_for_topic(topic: str) -> str:
    return curriculum_data.get_performance_criteria(topic)


@mcp.tool()
def get_resources_for_topic(topic: str) -> str:
    return curriculum_data.get_resources(topic)


@mcp.tool()
def get_tutorial_material_for_topic(topic: str) -> str:
    return curriculum_data.get_tutorial_material(topic)


if __name__ == "__main__":
    mcp.run(transport="stdio")
