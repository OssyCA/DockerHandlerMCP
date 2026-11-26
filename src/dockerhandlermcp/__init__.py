from fastmcp import FastMCP
import os
import httpx
import truststore

truststore.inject_into_ssl()
API_URL = os.environ.get("DOCKERHANDLER_API_URL", "http://localhost:5064")
API_KEY = os.environ["DOCKERHANDLER_API_KEY"]

docker_mcp = FastMCP("DockerHandler")

@docker_mcp.tool("health", description="Health check for DockerHandler")
def docker_handlerHealth():
    """
    Health check endpoint for DockerHandler.
    """
    response = httpx.get(url=f"{API_URL}/health", headers={"X-API-Key": f"{API_KEY}"})
    status = {"status": response.status_code, "message": response.text}
    return status

def main() -> None:
    docker_mcp.run()