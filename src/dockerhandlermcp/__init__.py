from fastmcp import FastMCP
import os
import httpx
import truststore

truststore.inject_into_ssl()
API_URL = os.environ.get("DOCKERHANDLER_API_URL", "http://localhost:5064")
API_KEY = os.environ["DOCKERHANDLER_API_KEY"]

client = httpx.Client(base_url=API_URL, headers={"X-Api-Key": API_KEY}, timeout=10)

docker_mcp = FastMCP("DockerHandler")


@docker_mcp.tool
def health() -> dict:
    """Check that the DockerHandler API and the Docker daemon are reachable."""
    response = client.get("/health")
    return {"status": response.status_code, "message": response.text}


@docker_mcp.tool
def list_containers() -> str:
    """List all containers managed by DockerHandler (running and stopped)."""
    response = client.get("/containers")
    response.raise_for_status()
    return response.text


@docker_mcp.tool
def get_container(container_id: str) -> str:
    """Get details about one container.

    Args:
        container_id: The container's id or name.
    """
    response = client.get(f"/containers/{container_id}")
    response.raise_for_status()
    return response.text


def main() -> None:
    docker_mcp.run()
