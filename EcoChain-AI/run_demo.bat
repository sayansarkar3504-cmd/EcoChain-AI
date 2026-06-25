@echo off
echo Starting EcoChain AI Demo...
echo.

echo [1/2] Starting MCP Server...
start cmd /k "python mcp_server/server.py"

echo [2/2] Starting Streamlit Dashboard...
start cmd /k "streamlit run app.py"

echo.
echo Both servers are starting in separate windows.
echo Please open the Streamlit URL in your browser if it doesn't open automatically.
echo You can use the data/vendors.csv as a sample upload.
pause
