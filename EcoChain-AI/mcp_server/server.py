from mcp.server.fastmcp import FastMCP
from .tools import get_vendor, get_vendor_history, get_invoice_data, calculate_risk_score, log_agent_action

# Create an MCP server instance
mcp = FastMCP("EcoChain_MCP")

# Register tools
@mcp.tool()
def fetch_vendor(vendor_name: str) -> str:
    """Retrieves the details of a specific vendor from the database."""
    return get_vendor(vendor_name)

@mcp.tool()
def fetch_vendor_history(vendor_name: str) -> str:
    """Retrieves the history and details of a specific vendor."""
    return get_vendor_history(vendor_name)

@mcp.tool()
def fetch_invoices(vendor_id: int) -> str:
    """Retrieves all invoice records for a specific vendor ID."""
    return get_invoice_data(vendor_id)

@mcp.tool()
def compute_risk_score(vendor_id: int) -> str:
    """Queries the database for the vendor's carbon and compliance scores to compute risk."""
    return calculate_risk_score(vendor_id)

@mcp.tool()
def log_action(agent_name: str, action: str) -> str:
    """Logs an agent's action to the audit_logs table."""
    return log_agent_action(agent_name, action)

if __name__ == "__main__":
    # Start the MCP server using stdio transport
    print("Starting EcoChain MCP Server...")
    mcp.run(transport="stdio")
