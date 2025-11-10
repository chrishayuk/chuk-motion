#!/bin/bash
# Script to verify all layout directories exist
for layout in HUDStyle Timeline PerformanceMultiCam Mosaic; do
  dir="src/chuk_mcp_remotion/components/layouts/$layout"
  if [ -d "$dir" ]; then
    echo "✓ $layout directory exists"
  else
    echo "✗ $layout directory missing"
  fi
done
