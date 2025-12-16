#!/usr/bin/env python3
"""
Remotion MCP Server - AI-powered video generation with design system approach

This module provides the async MCP server for Remotion video operations.
Supports both stdio (for Claude Desktop) and HTTP (for API access) transports.
"""

import logging
import os
import sys

logger = logging.getLogger(__name__)


def _init_artifact_store() -> bool:
    """
    Initialize the artifact store from environment variables.

    Checks for S3/Tigris configuration and sets up the global artifact store.
    This enables cloud storage for videos on Fly.io deployments.

    Returns:
        True if artifact store was initialized, False otherwise
    """
    # Check if we have S3 configuration (Tigris on Fly.io)
    provider = os.environ.get("CHUK_ARTIFACTS_PROVIDER", "memory")
    bucket = os.environ.get("BUCKET_NAME")
    redis_url = os.environ.get("REDIS_URL")

    # For S3 provider, we need bucket and AWS credentials
    if provider == "s3":
        aws_key = os.environ.get("AWS_ACCESS_KEY_ID")
        aws_secret = os.environ.get("AWS_SECRET_ACCESS_KEY")
        aws_endpoint = os.environ.get("AWS_ENDPOINT_URL_S3")

        if not all([bucket, aws_key, aws_secret]):
            logger.warning(
                "S3 provider configured but missing credentials. "
                "Set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and BUCKET_NAME."
            )
            return False

        logger.info(f"Initializing artifact store with S3 provider (bucket: {bucket})")
        logger.info(f"  Endpoint: {aws_endpoint}")
        logger.info(f"  Redis URL: {'configured' if redis_url else 'not configured'}")

    try:
        from chuk_artifacts import ArtifactStore
        from chuk_mcp_server import set_global_artifact_store

        # Create the artifact store with environment-based configuration
        store = ArtifactStore(
            storage_provider=provider,
            bucket=bucket,
            session_provider="redis" if redis_url else "memory",
        )

        # Set as global artifact store for chuk-mcp-server context
        set_global_artifact_store(store)

        logger.info(f"Artifact store initialized successfully (provider: {provider})")
        return True

    except Exception as e:
        logger.error(f"Failed to initialize artifact store: {e}")
        return False


# Initialize artifact store at module load time
_artifact_store_ready = _init_artifact_store()

# Import mcp instance from async server
from .async_server import mcp  # noqa: F401, E402

# The tools are registered via decorators in async_server.py
# They become available as soon as the module is imported


def main():
    """Main entry point for the MCP server.

    Automatically detects transport mode:
    - stdio: When stdin is piped or MCP_STDIO is set (for Claude Desktop)
    - HTTP: Default mode for API access
    """
    import argparse

    parser = argparse.ArgumentParser(description="Remotion MCP Server")
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["stdio", "http"],
        default=None,
        help="Transport mode (stdio for Claude Desktop, http for API)",
    )
    parser.add_argument(
        "--host", default="localhost", help="Host for HTTP mode (default: localhost)"
    )
    parser.add_argument("--port", type=int, default=8000, help="Port for HTTP mode (default: 8000)")

    args = parser.parse_args()

    # Determine transport mode
    if args.mode == "stdio":
        print("Remotion MCP Server starting in STDIO mode", file=sys.stderr)
        mcp.run(stdio=True)
    elif args.mode == "http":
        print(
            f"Remotion MCP Server starting in HTTP mode on {args.host}:{args.port}",
            file=sys.stderr,
        )
        mcp.run(host=args.host, port=args.port, stdio=False)
    else:
        # Auto-detect mode based on environment
        if os.environ.get("MCP_STDIO") or (not sys.stdin.isatty()):
            print("Remotion MCP Server starting in STDIO mode (auto-detected)", file=sys.stderr)
            mcp.run(stdio=True)
        else:
            print(
                f"Remotion MCP Server starting in HTTP mode on {args.host}:{args.port}",
                file=sys.stderr,
            )
            mcp.run(host=args.host, port=args.port, stdio=False)


if __name__ == "__main__":
    main()
