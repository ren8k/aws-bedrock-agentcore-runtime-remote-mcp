#!/bin/bash

# Function to generate MCP endpoint from agent ARN
get_mcp_endpoint() {
    local agent_arn="$1"
    local region="${2:-us-west-2}"  # Default to us-west-2 if not provided

    # URL encode the ARN: replace : with %3A and / with %2F
    local encoded_arn=$(echo "$agent_arn" | sed 's/:/%3A/g' | sed 's/\//%2F/g')

    # Construct the MCP endpoint URL
    echo "https://bedrock-agentcore.${region}.amazonaws.com/runtimes/${encoded_arn}/invocations?qualifier=DEFAULT"
}

# Load environment variables from .env file
if [ -f ../.env ]; then
    set -a
    source ../.env
    set +a
fi

# Check if required environment variables are set
if [ -z "$AGENT_ARN" ] || [ -z "$COGNITO_ACCESS_TOKEN" ]; then
    echo "Error: AGENT_ARN and COGNITO_ACCESS_TOKEN must be set in .env file"
    exit 1
fi

# Generate MCP_ENDPOINT from AGENT_ARN
MCP_ENDPOINT=$(get_mcp_endpoint "$AGENT_ARN" "${AWS_REGION:-us-west-2}")

echo "Generated MCP_ENDPOINT: $MCP_ENDPOINT"

claude mcp add --transport http \
    o3-mcp-server "$MCP_ENDPOINT" \
    --header "Authorization: Bearer $COGNITO_ACCESS_TOKEN"
