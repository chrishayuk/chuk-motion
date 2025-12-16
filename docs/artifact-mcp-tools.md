# Artifact-Based MCP Tools

## Overview

These MCP tools provide modern, async-native project management using **chuk-artifacts** for storage. Unlike the legacy `remotion_*` tools that use direct filesystem storage, these tools leverage the unified artifact storage system with support for multiple backends (memory, filesystem, S3, SQLite).

## Configuration

Set the storage provider via environment variable:

```bash
# Development (in-memory, ephemeral)
export CHUK_MOTION_STORAGE_PROVIDER=vfs-memory

# Local (filesystem, persistent)
export CHUK_MOTION_STORAGE_PROVIDER=vfs-filesystem

# Embedded (SQLite, portable)
export CHUK_MOTION_STORAGE_PROVIDER=vfs-sqlite

# Production (S3, cloud)
export CHUK_MOTION_STORAGE_PROVIDER=vfs-s3
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_S3_BUCKET=chuk-motion-artifacts
```

---

## Project Management Tools

### `artifact_create_project`

Create a new Remotion project with artifact storage.

**Parameters:**
- `name` (string, required): Project name
- `theme` (string, default: "tech"): Theme (tech, finance, education, lifestyle, gaming, minimal, business)
- `fps` (int, default: 30): Frames per second
- `width` (int, default: 1920): Video width in pixels
- `height` (int, default: 1080): Video height in pixels
- `scope` (string, default: "session"): Storage scope
  - `"session"` - Temporary (auto-deleted after TTL)
  - `"user"` - Persistent (user-owned)
  - `"sandbox"` - Shared (accessible to all users)
- `user_id` (string, optional): User ID (required for "user" scope)

**Returns:**
```json
{
  "success": true,
  "namespace_id": "ns_abc123",
  "name": "my_video",
  "theme": "tech",
  "fps": 30,
  "resolution": "1920x1080",
  "scope": "session",
  "grid_path": "grid/default/sess-123/ns_abc123",
  "provider": "vfs-filesystem"
}
```

**Example:**
```python
# Create temporary project (session scope)
project = await artifact_create_project(
    name="demo_video",
    theme="tech",
    scope="session"
)

# Create persistent user project
project = await artifact_create_project(
    name="my_tutorial",
    theme="education",
    scope="user",
    user_id="alice"
)

# Create shared template
project = await artifact_create_project(
    name="intro_template",
    theme="business",
    scope="sandbox"
)
```

---

### `artifact_get_project`

Get complete project information by namespace ID.

**Parameters:**
- `namespace_id` (string, required): The namespace ID from `artifact_create_project`

**Returns:**
```json
{
  "success": true,
  "namespace_id": "ns_abc123",
  "name": "my_video",
  "theme": "tech",
  "fps": 30,
  "width": 1920,
  "height": 1080,
  "total_duration_seconds": 45.5,
  "component_count": 12,
  "created_at": "2025-01-30T10:00:00Z",
  "updated_at": "2025-01-30T11:30:00Z",
  "scope": "user",
  "checkpoints": [
    {
      "checkpoint_id": "cp_123",
      "name": "v1.0",
      "description": "First draft",
      "created_at": "2025-01-30T10:30:00Z"
    }
  ]
}
```

**Example:**
```python
info = await artifact_get_project(namespace_id="ns_abc123")
```

---

## Checkpoint Management Tools

### `artifact_create_checkpoint`

Create a checkpoint (version snapshot) of the current project.

**Parameters:**
- `name` (string, required): Checkpoint name (e.g., "v1.0", "draft-1")
- `description` (string, optional): Description of this checkpoint

**Returns:**
```json
{
  "success": true,
  "checkpoint_id": "cp_123",
  "namespace_id": "ns_abc123",
  "name": "v1.0",
  "description": "First complete draft",
  "created_at": "2025-01-30T10:30:00Z"
}
```

**Example:**
```python
checkpoint = await artifact_create_checkpoint(
    name="v1.0",
    description="Ready for review"
)
```

---

### `artifact_list_checkpoints`

List all checkpoints for the current project.

**Parameters:** None

**Returns:**
```json
{
  "success": true,
  "namespace_id": "ns_abc123",
  "checkpoints": [
    {
      "checkpoint_id": "cp_123",
      "name": "v1.0",
      "description": "First draft",
      "created_at": "2025-01-30T10:00:00Z"
    },
    {
      "checkpoint_id": "cp_124",
      "name": "v1.1",
      "description": "Added animations",
      "created_at": "2025-01-30T11:00:00Z"
    }
  ]
}
```

**Example:**
```python
checkpoints = await artifact_list_checkpoints()
```

---

### `artifact_restore_checkpoint`

Restore the current project to a previous checkpoint.

⚠️ **WARNING:** This will replace the current project state with the checkpoint version. Create a new checkpoint before restoring to preserve your current work.

**Parameters:**
- `checkpoint_id` (string, required): The checkpoint ID to restore

**Returns:**
```json
{
  "success": true,
  "namespace_id": "ns_abc123",
  "checkpoint_id": "cp_123",
  "message": "Project restored successfully"
}
```

**Example:**
```python
# Save current state first
await artifact_create_checkpoint(name="pre-restore-backup")

# Restore previous version
result = await artifact_restore_checkpoint(checkpoint_id="cp_123")
```

---

## Render Tools

### `artifact_render_video`

Render the current project using Remotion CLI and automatically store as an artifact.

This tool:
1. Exports the project from VFS to a temporary directory
2. Installs npm dependencies
3. Runs Remotion CLI to render the video
4. Tracks progress during rendering
5. Optionally stores the rendered video as an artifact

**Parameters:**
- `composition_id` (string, optional): Composition ID to render (auto-detected if not provided)
- `output_format` (string, default: "mp4"): Output format (mp4, webm)
- `quality` (string, default: "high"): Quality preset (low, medium, high)
- `concurrency` (int, default: 4): Number of concurrent render threads
- `store_as_artifact` (bool, default: true): Whether to store the rendered video as an artifact

**Returns:**
```json
{
  "success": true,
  "composition_id": "my-video",
  "format": "mp4",
  "quality": "high",
  "resolution": "1920x1080",
  "fps": 30,
  "duration_seconds": 45.5,
  "file_size_bytes": 15728640,
  "render_id": "ns_render_xyz",
  "message": "Video rendered and stored as artifact"
}
```

**Example:**
```python
# Render with defaults (high quality, store as artifact)
result = await artifact_render_video()

# Custom render settings
result = await artifact_render_video(
    composition_id="custom-composition",
    output_format="webm",
    quality="medium",
    concurrency=8
)

# Render without storing as artifact
result = await artifact_render_video(
    quality="low",
    store_as_artifact=False  # Just renders, doesn't store
)
```

**Quality Presets:**
- `"low"` - Fast render, larger file size (CRF 28, fast preset)
- `"medium"` - Balanced quality and speed (CRF 23, medium preset)
- `"high"` - Best quality, slower render (CRF 18, slow preset)

---

### `artifact_store_render` (Deprecated)

⚠️ **DEPRECATED:** Use `artifact_render_video` instead for integrated rendering and storage.

Store an already-rendered video as an artifact.

**Parameters:**
- `video_data_path` (string, required): Path to the rendered video file
- `format` (string, default: "mp4"): Video format (mp4, webm)
- `codec` (string, optional): Video codec (h264, vp9)
- `bitrate_kbps` (int, optional): Video bitrate in kbps

**Returns:**
```json
{
  "success": true,
  "render_id": "ns_render_xyz",
  "project_id": "ns_abc123",
  "format": "mp4",
  "size_bytes": 15728640,
  "duration_seconds": 45.5,
  "checksum": "sha256:abc123...",
  "grid_path": "grid/default/user-alice/ns_render_xyz"
}
```

**Example:**
```python
# Only use if you already have a rendered video file
render = await artifact_store_render(
    video_data_path="/path/to/output.mp4",
    format="mp4",
    codec="h264",
    bitrate_kbps=5000
)
```

---

## Workflow Examples

### Complete Video Creation Workflow

```python
# 1. Create project
project = await artifact_create_project(
    name="tutorial_video",
    theme="education",
    scope="user",
    user_id="alice"
)

namespace_id = project["namespace_id"]

# 2. Build composition (using existing component tools)
# Add scenes, charts, animations, etc...
# await remotion_add_component(...)

# 3. Create checkpoint before major changes
checkpoint1 = await artifact_create_checkpoint(
    name="draft-1",
    description="Initial composition complete"
)

# 4. Make changes...
# Add more components, adjust timing, etc.

# 5. Create another checkpoint
checkpoint2 = await artifact_create_checkpoint(
    name="draft-2",
    description="Added animations and transitions"
)

# 6. Render video with automatic artifact storage
render_result = await artifact_render_video(
    quality="high",
    output_format="mp4",
    concurrency=8
)

print(f"Rendered: {render_result['resolution']} @ {render_result['fps']} fps")
print(f"Duration: {render_result['duration_seconds']} seconds")
print(f"File size: {render_result['file_size_bytes'] / 1024 / 1024:.2f} MB")
print(f"Render ID: {render_result['render_id']}")

# 7. Get final project info with all checkpoints
final_info = await artifact_get_project(namespace_id=namespace_id)
```

### Version Control Workflow

```python
# Save current state
await artifact_create_checkpoint(
    name="before-experiment",
    description="Stable version before trying new approach"
)

# Make experimental changes...

# If experiment fails, restore
await artifact_restore_checkpoint(checkpoint_id="cp_before")

# If experiment succeeds, save it
await artifact_create_checkpoint(
    name="experiment-success",
    description="New approach works great"
)
```

### Multi-User Collaboration

```python
# User Alice creates a project
alice_project = await artifact_create_project(
    name="team_video",
    theme="business",
    scope="user",
    user_id="alice"
)

# Alice creates checkpoints as she works
await artifact_create_checkpoint(
    name="alice-draft-1",
    description="Initial scenes"
)

# Later, Alice can share the namespace_id with Bob
# Bob can load the project (if permissions allow)
project_info = await artifact_get_project(
    namespace_id=alice_project["namespace_id"]
)
```

---

## Comparison with Legacy Tools

| Feature | Legacy (`remotion_*`) | Modern (`artifact_*`) |
|---------|----------------------|---------------------|
| **Storage** | Direct filesystem | chuk-artifacts (VFS-backed) |
| **Async** | ❌ (uses run_in_executor) | ✅ (native async/await) |
| **Type Safety** | ❌ (dicts) | ✅ (Pydantic models) |
| **Versioning** | ❌ | ✅ (checkpoints) |
| **Multi-tenant** | ❌ | ✅ (scope-based isolation) |
| **Cloud Storage** | ❌ | ✅ (S3 support) |
| **Scope Isolation** | ❌ | ✅ (SESSION/USER/SANDBOX) |
| **Providers** | Filesystem only | Memory, Filesystem, S3, SQLite |
| **Integrated Render** | ❌ (manual) | ✅ (artifact_render_video) |
| **Progress Tracking** | ❌ | ✅ (real-time render progress) |
| **Auto-Storage** | ❌ (manual storage) | ✅ (automatic artifact storage) |

---

## Storage Scopes Explained

### SESSION Scope
- **Lifecycle:** Temporary (auto-deleted after TTL, default 24 hours)
- **Use Cases:** Quick experiments, temporary previews, draft renders
- **Grid Path:** `grid/default/sess-{session_id}/{namespace_id}`

### USER Scope
- **Lifecycle:** Persistent (user-owned, survives restarts)
- **Use Cases:** Personal projects, final renders, saved work
- **Grid Path:** `grid/default/user-{user_id}/{namespace_id}`
- **Requires:** `user_id` parameter

### SANDBOX Scope
- **Lifecycle:** Persistent (shared across all users)
- **Use Cases:** Templates, examples, shared resources
- **Grid Path:** `grid/default/shared/{namespace_id}`

---

## Error Handling

All tools return JSON with `success` field:

```python
# Success
{
  "success": true,
  "namespace_id": "ns_abc123",
  ...
}

# Error
{
  "error": "No active project. Create a project first."
}
```

Common errors:
- `"Invalid scope 'xyz'. Must be 'session', 'user', or 'sandbox'"`
- `"user_id is required for USER scope"`
- `"No active project. Create a project first."`
- `"Namespace not found: ns_xyz"`

---

## Best Practices

1. **Use SESSION scope for experiments** - Auto-cleanup prevents storage bloat
2. **Use USER scope for real work** - Persistent storage with user isolation
3. **Create checkpoints before major changes** - Easy rollback if needed
4. **Use descriptive checkpoint names** - Makes version history clear
5. **Use `artifact_render_video` for rendering** - Integrated rendering with automatic artifact storage
6. **Adjust quality/concurrency for your needs** - Balance render time vs quality
7. **Create checkpoint before rendering** - Preserve pre-render state
8. **Monitor render progress** - RemotionRenderer provides real-time progress updates

---

## Future Enhancements

- [ ] Asset management tools (store/retrieve images, audio, fonts)
- [ ] Batch operations (create multiple checkpoints, bulk restores)
- [ ] Search and filter (find projects by theme, date, user)
- [ ] Export/import (share projects across systems)
- [ ] CDN integration (serve renders from CDN)
- [ ] Webhook notifications (notify on render completion)

---

## See Also

- [Artifact Storage Implementation](../ARTIFACT_STORAGE_IMPLEMENTATION.md)
- [ArtifactStorageManager API](../src/chuk_motion/storage/artifact_storage.py)
- [AsyncProjectManager API](../src/chuk_motion/utils/async_project_manager.py)
- [Project Management Roadmap](./project-management.md)
