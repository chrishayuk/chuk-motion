# Virtual Filesystem Integration

The Remotion MCP Server uses [chuk-virtual-fs](https://github.com/chrishayuk/chuk-virtual-fs) for all file operations, providing a unified, flexible, and secure approach to file management.

## Overview

The virtual filesystem (VFS) abstracts file operations behind a consistent API that works with multiple storage providers. This enables:

- **Flexibility**: Switch between file, memory, SQLite, S3, and other providers
- **Security**: Built-in access controls and security profiles
- **Testability**: Easy mocking with memory provider for tests
- **Portability**: Same code works across different storage backends

## Architecture

```
┌─────────────────────────────────────┐
│   Remotion MCP Server               │
├─────────────────────────────────────┤
│  - TokenManager                     │
│  - ThemeManager                     │
│  - ProjectManager                   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   AsyncVirtualFileSystem            │
├─────────────────────────────────────┤
│  - Unified API                      │
│  - Security Controls                │
│  - Provider Abstraction             │
└──────────────┬──────────────────────┘
               │
        ┌──────┴──────┬──────────┬────────┐
        ▼             ▼          ▼        ▼
    ┌──────┐    ┌─────────┐ ┌──────┐ ┌────┐
    │ File │    │ Memory  │ │SQLite│ │ S3 │
    └──────┘    └─────────┘ └──────┘ └────┘
```

## Usage in chuk-motion

### Initialization

The virtual filesystem is initialized in `server.py`:

```python
from chuk_virtual_fs import AsyncVirtualFileSystem

# Create VFS instance with file provider
vfs = AsyncVirtualFileSystem(provider="file")

# Pass to managers
token_manager = TokenManager(vfs)
theme_manager = ThemeManager(vfs)
```

### Token Management with VFS

The `TokenManager` uses VFS for all token import/export operations:

```python
# Export typography tokens
await token_manager.export_typography_tokens(
    file_path="my_typography.json"
)

# Import typography tokens
await token_manager.import_typography_tokens(
    file_path="my_typography.json",
    merge=True
)

# Export all tokens to directory
results = await token_manager.export_all_tokens(
    output_dir="my_design_system"
)
```

**VFS Operations Used:**
- `write_file()` - Write JSON token data
- `read_text()` - Read JSON token data
- `mkdir()` - Create directories for organized exports

### Theme Management with VFS

The `ThemeManager` uses VFS for theme import/export:

```python
# Export theme
await theme_manager.export_theme(
    theme_key="tech",
    file_path="tech_theme.json"
)

# Import theme
await theme_manager.import_theme(
    file_path="custom_theme.json",
    theme_key="my_custom"
)
```

**VFS Operations Used:**
- `write_file()` - Write theme JSON
- `read_text()` - Read theme JSON

## Storage Providers

### File Provider (Default)

Uses the local filesystem for storage.

```python
vfs = AsyncVirtualFileSystem(provider="file")
```

**Use Cases:**
- Development
- Local project management
- Direct file system access needed

**Features:**
- Full filesystem access
- No additional setup required
- Fast read/write operations

### Memory Provider

Stores files in memory (RAM).

```python
vfs = AsyncVirtualFileSystem(provider="memory")
```

**Use Cases:**
- Unit testing
- Temporary file operations
- Fast ephemeral storage

**Features:**
- Lightning fast
- No disk I/O
- Automatic cleanup on close
- Perfect for tests

### SQLite Provider

Stores files in a SQLite database.

```python
vfs = AsyncVirtualFileSystem(
    provider="sqlite",
    db_path="remotion_files.db"
)
```

**Use Cases:**
- Embedded databases
- Single-file deployments
- ACID transaction requirements

**Features:**
- Transactional operations
- Single file storage
- Built-in indexing

### S3 Provider

Stores files in AWS S3 or S3-compatible storage.

```python
vfs = AsyncVirtualFileSystem(
    provider="s3",
    bucket_name="my-remotion-projects",
    aws_access_key_id="...",
    aws_secret_access_key="..."
)
```

**Use Cases:**
- Cloud deployments
- Distributed systems
- Multi-region access
- Large-scale storage

**Features:**
- Scalable storage
- High availability
- Global access
- Cost-effective

## Security Features

The VFS includes built-in security controls:

### Security Profiles

```python
# Read-only access
vfs = AsyncVirtualFileSystem(
    provider="file",
    security_profile="readonly"
)

# Strict security (restricted paths)
vfs = AsyncVirtualFileSystem(
    provider="file",
    security_profile="strict"
)

# Untrusted environment (maximum restrictions)
vfs = AsyncVirtualFileSystem(
    provider="file",
    security_profile="untrusted"
)
```

### Path Restrictions

Limit access to specific directories:

```python
vfs = AsyncVirtualFileSystem(
    provider="file",
    allowed_paths=["/home/user/projects", "/tmp/exports"]
)
```

### File Size Quotas

Set maximum file sizes:

```python
vfs = AsyncVirtualFileSystem(
    provider="file",
    max_file_size=10 * 1024 * 1024  # 10MB limit
)
```

## API Reference

### Common Operations

#### Write File
```python
await vfs.write_file("path/to/file.json", json_content)
```

#### Read File
```python
content = await vfs.read_text("path/to/file.json")
data = json.loads(content)
```

#### Create Directory
```python
await vfs.mkdir("path/to/directory")
```

#### List Directory
```python
files = await vfs.ls("path/to/directory")
```

#### Check Existence
```python
exists = await vfs.exists("path/to/file.json")
```

#### Copy File
```python
await vfs.cp("source.json", "destination.json")
```

#### Move File
```python
await vfs.mv("old_location.json", "new_location.json")
```

#### Delete File
```python
await vfs.rm("path/to/file.json")
```

#### Find Files
```python
results = await vfs.find("*.json", path="/themes", recursive=True)
```

## Testing with VFS

The memory provider makes testing simple:

```python
import pytest
from chuk_virtual_fs import AsyncVirtualFileSystem

@pytest.fixture
async def vfs():
    """Create memory-based VFS for testing."""
    async with AsyncVirtualFileSystem(provider="memory") as fs:
        yield fs

@pytest.mark.asyncio
async def test_token_export(vfs):
    """Test token export with memory VFS."""
    token_manager = TokenManager(vfs)

    # Export tokens to memory
    result = await token_manager.export_typography_tokens(
        file_path="test_tokens.json"
    )

    # Verify file exists in memory
    assert await vfs.exists("test_tokens.json")

    # Read and verify content
    content = await vfs.read_text("test_tokens.json")
    data = json.loads(content)
    assert "font_families" in data
```

## Advanced Features

### Snapshots

Create point-in-time snapshots:

```python
# Create snapshot
snapshot_id = await vfs.create_snapshot("v1.0")

# Restore snapshot
await vfs.restore_snapshot(snapshot_id)

# List snapshots
snapshots = await vfs.list_snapshots()
```

### Templates

Use file templates:

```python
# Register template
await vfs.register_template(
    "video_config",
    content=config_template,
    variables=["project_name", "fps", "resolution"]
)

# Apply template
await vfs.apply_template(
    "video_config",
    output_path="config.json",
    variables={
        "project_name": "my_video",
        "fps": 30,
        "resolution": "1080p"
    }
)
```

### Streaming

Stream large files efficiently:

```python
# Stream write
async with vfs.open_stream("large_file.json", mode="w") as stream:
    await stream.write(chunk1)
    await stream.write(chunk2)

# Stream read
async with vfs.open_stream("large_file.json", mode="r") as stream:
    chunk = await stream.read(1024)
```

## Migration Between Providers

The VFS makes it easy to migrate between providers:

```python
# Export from file provider
async with AsyncVirtualFileSystem(provider="file") as file_vfs:
    content = await file_vfs.read_text("themes/tech_theme.json")

# Import to S3 provider
async with AsyncVirtualFileSystem(provider="s3") as s3_vfs:
    await s3_vfs.write_file("themes/tech_theme.json", content)
```

## Best Practices

1. **Use Context Managers**: Always use `async with` for automatic cleanup
   ```python
   async with AsyncVirtualFileSystem(provider="file") as vfs:
       # Operations here
       pass
   # VFS automatically closed
   ```

2. **Handle Errors Gracefully**: VFS operations can fail
   ```python
   try:
       await vfs.read_text("config.json")
   except FileNotFoundError:
       # Handle missing file
       pass
   ```

3. **Choose the Right Provider**:
   - Development: `file`
   - Testing: `memory`
   - Production: `s3` or `sqlite`

4. **Set Appropriate Security**: Use strict profiles in production
   ```python
   vfs = AsyncVirtualFileSystem(
       provider="file",
       security_profile="strict",
       allowed_paths=["/app/projects"]
   )
   ```

5. **Use Relative Paths**: Avoid absolute paths when possible
   ```python
   # Good
   await vfs.write_file("themes/custom.json", data)

   # Avoid
   await vfs.write_file("/home/user/themes/custom.json", data)
   ```

## Troubleshooting

### Permission Errors
```
Error: Permission denied
```
**Solution**: Check security profile and allowed_paths settings

### File Not Found
```
Error: File not found: themes/custom.json
```
**Solution**: Ensure file exists or create parent directories first

### Provider Connection Issues
```
Error: Could not connect to S3 bucket
```
**Solution**: Verify credentials and bucket configuration

## See Also

- [chuk-virtual-fs Documentation](https://github.com/chrishayuk/chuk-virtual-fs)
- [Project Management](project-management.md) - Using VFS for projects
- [Token System](token-system.md) - Token import/export with VFS
- [Themes Guide](themes.md) - Theme management with VFS
