# Project Management

The Remotion MCP Server provides comprehensive project management tools for creating, organizing, and generating video projects using the virtual filesystem.

## Overview

Project management in chuk-motion handles:
- Creating new Remotion projects
- Managing project structure and configuration
- Organizing components and compositions
- Building and rendering video projects
- Listing and discovering existing projects

## Project Structure

Each Remotion project follows this structure:

```
project-name/
├── package.json           # Project dependencies
├── remotion.config.ts     # Remotion configuration
├── tsconfig.json          # TypeScript configuration
├── .gitignore            # Git ignore rules
└── src/
    ├── index.ts          # Entry point
    ├── Root.tsx          # Root composition
    ├── VideoComposition.tsx  # Generated composition
    └── components/
        ├── TitleScene.tsx
        ├── LowerThird.tsx
        └── ...           # Other generated components
```

## MCP Tools

### remotion_create_project

Create a new Remotion video project with theme and configuration.

**Parameters:**
- `name` (required): Project name (used as directory name)
- `theme` (optional): Theme to use (default: "tech")
  - Options: tech, finance, education, lifestyle, gaming, minimal, business
- `fps` (optional): Frames per second (default: 30)
- `width` (optional): Video width in pixels (default: 1920)
- `height` (optional): Video height in pixels (default: 1080)

**Example:**
```python
await remotion_create_project(
    name="my_video_project",
    theme="tech",
    fps=30,
    width=1920,
    height=1080
)
```

**Returns:**
```json
{
  "name": "my_video_project",
  "path": "/path/to/remotion-projects/my_video_project",
  "theme": "tech",
  "fps": "30",
  "resolution": "1920x1080"
}
```

### remotion_list_projects

List all Remotion projects in the workspace.

**Example:**
```python
await remotion_list_projects()
```

**Returns:**
```json
[
  {
    "name": "project1",
    "path": "/path/to/remotion-projects/project1"
  },
  {
    "name": "project2",
    "path": "/path/to/remotion-projects/project2"
  }
]
```

### remotion_get_composition_info

Get information about the current active composition including all components, timeline, and configuration.

**Example:**
```python
await remotion_get_composition_info()
```

**Returns:**
```json
{
  "name": "my_video_project",
  "path": "/path/to/project",
  "composition": {
    "fps": 30,
    "width": 1920,
    "height": 1080,
    "theme": "tech",
    "components": [
      {
        "type": "TitleScene",
        "start_frame": 0,
        "duration_frames": 90
      }
    ],
    "total_duration": 5.0
  }
}
```

## Adding Components to Projects

Once a project is created, you can add video components:

### remotion_add_title_scene

Add an animated title scene to the composition.

**Parameters:**
- `text` (required): Main title text
- `subtitle` (optional): Subtitle text
- `duration_seconds` (optional): Display duration (default: 3.0)
- `variant` (optional): Style variant (minimal, standard, bold, kinetic)
- `animation` (optional): Animation style (fade_zoom, slide_up, typewriter, blur_in, split)

**Example:**
```python
await remotion_add_title_scene(
    text="The Future of AI",
    subtitle="Transforming Technology",
    duration_seconds=3.0,
    variant="bold",
    animation="fade_zoom"
)
```

### remotion_add_lower_third

Add a lower third overlay (name plate/caption) to the video.

**Parameters:**
- `name` (required): Main name/text to display
- `title` (optional): Subtitle/title text
- `start_time` (optional): When to show (seconds, default: 0.0)
- `duration` (optional): How long to show (seconds, default: 5.0)
- `variant` (optional): Style variant (minimal, standard, glass, bold, animated)
- `position` (optional): Screen position (bottom_left, bottom_center, bottom_right, top_left, top_center)

**Example:**
```python
await remotion_add_lower_third(
    name="Dr. Sarah Chen",
    title="AI Researcher, Stanford",
    start_time=2.0,
    duration=5.0,
    variant="glass",
    position="bottom_left"
)
```

## Generating Video Files

### remotion_generate_video

Generate all TSX components, update the composition, and write files to the project directory.

**Example:**
```python
result = await remotion_generate_video()
```

**Returns:**
```json
{
  "status": "success",
  "project": {
    "name": "my_video_project",
    "path": "/path/to/project"
  },
  "generated_files": [
    "/path/to/project/src/components/TitleScene.tsx",
    "/path/to/project/src/components/LowerThird.tsx",
    "/path/to/project/src/VideoComposition.tsx"
  ],
  "next_steps": [
    "cd /path/to/project",
    "npm install",
    "npm start  # Opens Remotion Studio",
    "npm run build  # Renders the video"
  ]
}
```

## Virtual Filesystem Integration

All project management operations use the virtual filesystem (chuk-virtual-fs) for file operations. This provides:

1. **Provider Flexibility**: Switch between file, memory, SQLite, S3, etc.
2. **Security**: Built-in security profiles and access controls
3. **Testability**: Easy mocking and testing with memory provider
4. **Consistency**: Unified API across different storage backends

See [Virtual Filesystem Guide](virtual-filesystem.md) for more details.

## Complete Workflow Example

Here's a complete workflow for creating a video project:

```python
# 1. Create project
await remotion_create_project(
    name="tech_tutorial",
    theme="tech",
    fps=30
)

# 2. Add title scene
await remotion_add_title_scene(
    text="React Hooks Tutorial",
    subtitle="Master useState and useEffect",
    duration_seconds=3.0,
    variant="bold",
    animation="fade_zoom"
)

# 3. Add lower third for speaker
await remotion_add_lower_third(
    name="Alex Johnson",
    title="Senior React Developer",
    start_time=3.5,
    duration=5.0,
    variant="glass"
)

# 4. Get composition info
info = await remotion_get_composition_info()
print(f"Total duration: {info['composition']['total_duration']} seconds")

# 5. Generate video files
result = await remotion_generate_video()
print(f"Generated {len(result['generated_files'])} files")

# 6. Build the video
# Run the commands from result['next_steps'] in terminal
```

## Project Configuration

### Theme Selection

Choose a theme that matches your content type:
- **tech**: Modern tech aesthetic (code, tutorials, tech reviews)
- **finance**: Professional finance theme (investing, trading, business)
- **education**: Friendly education theme (teaching, explainers, courses)
- **lifestyle**: Warm lifestyle theme (vlogs, lifestyle, wellness)
- **gaming**: High-energy gaming theme (gaming, esports, streams)
- **minimal**: Clean minimal theme (professional, corporate, timeless)
- **business**: Professional business theme (corporate, presentations, B2B)

### Video Settings

**Resolution Options:**
- 1080p: 1920x1080 (standard HD)
- 4K: 3840x2160 (ultra HD)
- 720p: 1280x720 (HD)

**Frame Rate:**
- 24 fps: Cinematic feel
- 30 fps: Standard video (recommended)
- 60 fps: Smooth motion (gaming, sports)

## Best Practices

1. **Choose the right theme**: Select a theme that matches your content type
2. **Plan your composition**: Sketch out your video structure before creating components
3. **Use consistent timing**: Keep animations and transitions consistent
4. **Test incrementally**: Generate and preview after adding each major component
5. **Version control**: Use git to track project changes
6. **Leverage tokens**: Use design tokens for consistent styling across projects

## Troubleshooting

### Project Already Exists
```
Error: Project 'my_video' already exists
```
**Solution**: Choose a different project name or delete the existing project

### No Active Project
```
Error: No active project. Create a project first.
```
**Solution**: Call `remotion_create_project()` before adding components

### Missing Dependencies
```
Error: Cannot find module '@remotion/cli'
```
**Solution**: Run `npm install` in the project directory

## CHUK Artifacts Integration

### Overview

`chuk-motion` will integrate with [chuk-artifacts](https://github.com/chrishayuk/chuk-artifacts) to provide a **unified VFS-backed storage substrate** for all project files, rendered videos, assets, and artifacts. This integration enables:

- **Namespace-based storage** for projects (WORKSPACE) and renders (BLOB)
- **Scope-based isolation** (SESSION, USER, SANDBOX)
- **Provider flexibility** (memory, filesystem, S3, SQLite)
- **Checkpoint versioning** for projects and renders
- **Multi-tenancy** with automatic access control
- **Production scalability** across different storage backends

### Architecture

```
chuk-motion Storage Architecture (with chuk-artifacts)
======================================================

┌─────────────────────────────────────────────────────────────────┐
│                       chuk-motion MCP Server                     │
│                                                                   │
│  • remotion_create_project → WORKSPACE namespace                │
│  • remotion_render_video → BLOB namespace (rendered MP4)        │
│  • remotion_store_asset → BLOB namespace (images, audio)        │
│  • remotion_checkpoint_project → checkpoint namespace           │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       │ ArtifactStore API
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                        chuk-artifacts                            │
│                  (Unified Namespace Management)                  │
│                                                                   │
│  WORKSPACE namespaces:                                           │
│  • Remotion project files (TSX, config, package.json)           │
│  • Multi-file directory trees                                    │
│  • Full VFS access (ls, cp, mv, mkdir, find)                    │
│                                                                   │
│  BLOB namespaces:                                                │
│  • Rendered videos (MP4, WebM)                                   │
│  • Thumbnails and previews                                       │
│  • Media assets (images, audio, fonts)                          │
│  • Single file storage with metadata                             │
│                                                                   │
│  Storage Scopes:                                                 │
│  • SESSION: Ephemeral renders, previews (TTL cleanup)           │
│  • USER: Personal projects and renders (persistent)             │
│  • SANDBOX: Shared templates and resources (all users)          │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       │ VFS Provider API
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    chuk-virtual-fs                               │
│                  (Unified VFS Layer)                             │
│                                                                   │
│  Provider-agnostic file operations:                              │
│  • ls(), mkdir(), rm(), cp(), mv()                              │
│  • read_file(), write_file()                                    │
│  • find(), batch operations                                     │
│  • Metadata management                                          │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       │ Storage Provider Selection
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Storage Providers                              │
│                                                                   │
│  Development:    vfs-memory (fast, ephemeral)                   │
│  Local:          vfs-filesystem (persistent, local)             │
│  Embedded:       vfs-sqlite (portable, queryable)               │
│  Production:     vfs-s3 (cloud, distributed, scalable)          │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
              grid/{sandbox}/{scope}/{namespace_id}/
```

### Namespace Types

#### WORKSPACE Namespaces (Project Files)

Each Remotion project becomes a WORKSPACE namespace:

```python
# Create project as WORKSPACE namespace
workspace = await artifact_store.create_namespace(
    type=NamespaceType.WORKSPACE,
    name="my_video_project",
    scope=StorageScope.USER,
    user_id="alice"
)

# Project files stored in namespace
grid/default/user-alice/{namespace_id}/
├── .workspace                 # Metadata
├── package.json
├── remotion.config.ts
├── tsconfig.json
└── src/
    ├── index.ts
    ├── Root.tsx
    ├── VideoComposition.tsx
    └── components/
        ├── TitleScene.tsx
        └── LowerThird.tsx

# Get VFS for project operations
vfs = artifact_store.get_namespace_vfs(workspace.namespace_id)
files = await vfs.ls("/src/components")
```

#### BLOB Namespaces (Rendered Videos & Assets)

Rendered videos and assets stored as BLOB namespaces:

```python
# Store rendered video as BLOB
render_blob = await artifact_store.create_namespace(
    type=NamespaceType.BLOB,
    scope=StorageScope.USER,
    user_id="alice"
)

# Write MP4 data
await artifact_store.write_namespace(
    render_blob.namespace_id,
    data=mp4_bytes
)

# Add metadata
vfs = artifact_store.get_namespace_vfs(render_blob.namespace_id)
await vfs.set_metadata("/_data", {
    "project_id": workspace.namespace_id,
    "format": "mp4",
    "resolution": "1920x1080",
    "fps": 30,
    "duration_seconds": 45.5,
    "render_date": "2025-01-30"
})
```

### Storage Scopes

| Scope | Use Case | Lifecycle | Grid Path |
|-------|----------|-----------|-----------|
| **SESSION** | Temporary previews, draft renders | Ephemeral (session lifetime) | `grid/default/sess-{session_id}/{ns_id}` |
| **USER** | Personal projects, final renders | Persistent (user-owned) | `grid/default/user-{user_id}/{ns_id}` |
| **SANDBOX** | Shared templates, example projects | Persistent (shared) | `grid/default/shared/{ns_id}` |

**Examples:**

```python
# Session-scoped preview (auto-cleanup when session ends)
preview = await artifact_store.create_namespace(
    type=NamespaceType.BLOB,
    scope=StorageScope.SESSION,
    ttl_hours=24  # Auto-delete after 24 hours
)

# User-scoped project (persistent)
project = await artifact_store.create_namespace(
    type=NamespaceType.WORKSPACE,
    name="my_tutorial_video",
    scope=StorageScope.USER,
    user_id="alice"
)

# Sandbox-scoped template (shared with all users)
template = await artifact_store.create_namespace(
    type=NamespaceType.WORKSPACE,
    name="tech_intro_template",
    scope=StorageScope.SANDBOX
)
```

### Checkpoint System

Version control for projects and renders using checkpoints:

```python
# Create checkpoint of project
checkpoint = await artifact_store.checkpoint_namespace(
    workspace.namespace_id,
    name="v1.0-ready-for-review",
    description="All animations complete, awaiting feedback"
)

# Make changes to project...
await artifact_store.write_namespace(
    workspace.namespace_id,
    path="/src/VideoComposition.tsx",
    data=updated_composition
)

# Restore from checkpoint if needed
await artifact_store.restore_namespace(
    workspace.namespace_id,
    checkpoint.checkpoint_id
)

# List all checkpoints
checkpoints = await artifact_store.list_checkpoints(workspace.namespace_id)
# [
#   {"id": "cp_123", "name": "v1.0-ready-for-review", "created": "2025-01-30T10:00:00Z"},
#   {"id": "cp_124", "name": "v1.1-final", "created": "2025-01-30T14:30:00Z"}
# ]
```

### Asset Management

Media assets (images, audio, fonts) stored as BLOB namespaces with metadata:

```python
# Store image asset
image_asset = await artifact_store.create_namespace(
    type=NamespaceType.BLOB,
    scope=StorageScope.USER,
    user_id="alice"
)

await artifact_store.write_namespace(
    image_asset.namespace_id,
    data=image_bytes
)

# Add searchable metadata
vfs = artifact_store.get_namespace_vfs(image_asset.namespace_id)
await vfs.set_metadata("/_data", {
    "asset_type": "image",
    "mime_type": "image/png",
    "width": 1920,
    "height": 1080,
    "tags": ["background", "tech", "gradient"],
    "project_ids": [workspace.namespace_id]
})

# Search for assets by metadata
python_files = await vfs.find(pattern="*.png", path="/", recursive=True)
```

### Production Deployment Patterns

#### Development (Memory Provider)

```python
# Fast, ephemeral storage for development
export ARTIFACT_PROVIDER=vfs-memory
export SESSION_PROVIDER=memory

store = ArtifactStore()  # Uses memory by default
```

#### Local Deployment (Filesystem Provider)

```python
# Persistent local storage
export ARTIFACT_PROVIDER=vfs-filesystem
export VFS_ROOT_PATH=/var/chuk-motion/artifacts

# Projects and renders stored locally
# Good for: Single-user installs, edge devices
```

#### Embedded Deployment (SQLite Provider)

```python
# Portable database storage
export ARTIFACT_PROVIDER=vfs-sqlite
export SQLITE_DB_PATH=/data/chuk-motion.db

# Single file, queryable
# Good for: Desktop apps, portable installs
```

#### Production Cloud (S3 Provider)

```python
# Scalable cloud storage with Redis sessions
export ARTIFACT_PROVIDER=vfs-s3
export SESSION_PROVIDER=redis
export AWS_S3_BUCKET=chuk-motion-artifacts
export REDIS_URL=redis://prod-redis:6379/0

# Multi-tenant, distributed, scalable
# Good for: SaaS, multi-user platforms
```

#### Hybrid Deployment

```python
# Different scopes, different backends
# SESSION: vfs-memory (fast ephemeral)
# USER: vfs-s3 (persistent cloud)
# SANDBOX: vfs-filesystem (local shared templates)

await artifact_store.create_namespace(
    type=NamespaceType.BLOB,
    scope=StorageScope.SESSION,
    provider_type="vfs-memory"  # Fast preview renders
)

await artifact_store.create_namespace(
    type=NamespaceType.WORKSPACE,
    scope=StorageScope.USER,
    provider_type="vfs-s3"  # User projects in cloud
)
```

### Migration Path

**Current Architecture:**
```
remotion-projects/
├── project1/
│   ├── package.json
│   └── src/...
└── project2/
    ├── package.json
    └── src/...
```

**Target Architecture (with chuk-artifacts):**
```
grid/default/
├── sess-{session_id}/
│   └── {namespace_id}/  # Temporary preview renders (SESSION)
├── user-{user_id}/
│   ├── {namespace_id}/  # User project workspace (USER)
│   └── {namespace_id}/  # User rendered video blob (USER)
└── shared/
    └── {namespace_id}/  # Shared template workspace (SANDBOX)
```

### Benefits

1. **Multi-tenancy**: Automatic user/session isolation
2. **Scalability**: Switch storage backends via configuration
3. **Versioning**: Built-in checkpoint system for projects and renders
4. **Cloud-native**: S3 backend for distributed deployments
5. **Testability**: Memory provider for instant testing
6. **Consistency**: Same storage API as chuk-ai-planner, chuk-mcp-server
7. **Asset Management**: Metadata-based search and organization
8. **Production-ready**: Grid architecture, access control, TTL cleanup

## Roadmap

### Phase 1: Foundation ✅ COMPLETE
- ✅ Design token system (colors, typography, motion, spacing)
- ✅ Component registry with 51 components
- ✅ 7 YouTube-optimized themes
- ✅ Discovery tools for LLMs
- ✅ Track-based timeline system
- ✅ Platform safe margin support

### Phase 2: Generation ✅ COMPLETE
- ✅ TSX component generation with Jinja2
- ✅ Remotion project scaffolding
- ✅ Composition builder with ComponentInstance
- ✅ ProjectManager API
- ✅ Time string parsing ("1s", "500ms")

### Phase 3: Rendering & Artifact Storage 🚧 IN PROGRESS
- 🔲 **Remotion render integration via CLI**
- 🔲 **chuk-artifacts integration for rendered videos**
  - 🔲 Store renders as BLOB namespaces
  - 🔲 Metadata tracking (resolution, fps, duration, format)
  - 🔲 Session-scoped temporary renders with TTL
  - 🔲 User-scoped persistent renders
- 🔲 **Export to MP4/WebM as artifacts**
  - 🔲 Streaming writes for large files
  - 🔲 Checksum validation
  - 🔲 Format conversion support
- 🔲 **Thumbnail generation**
  - 🔲 Auto-generate thumbnails from renders
  - 🔲 Store thumbnails as BLOB namespaces
  - 🔲 Multiple thumbnail sizes (small, medium, large)
- 🔲 **Preview generation**
  - 🔲 Low-resolution preview renders
  - 🔲 TTL-based cleanup for previews
  - 🔲 Session-scoped preview storage

### Phase 3.5: Storage Architecture Migration 🆕 PLANNED
- 🔲 **Migrate from filesystem to chuk-artifacts namespaces**
  - 🔲 Replace `remotion-projects/` directory with WORKSPACE namespaces
  - 🔲 Update ProjectManager to use ArtifactStore API
  - 🔲 Migrate existing projects to namespaces
- 🔲 **WORKSPACE namespaces for project files**
  - 🔲 Project creation as WORKSPACE namespace
  - 🔲 VFS-backed project file operations
  - 🔲 Grid-based project organization
- 🔲 **BLOB namespaces for rendered videos**
  - 🔲 Store MP4/WebM renders as blobs
  - 🔲 Metadata for render tracking
  - 🔲 Batch render operations
- 🔲 **Scope-based isolation**
  - 🔲 SESSION scope for temporary work
  - 🔲 USER scope for persistent projects
  - 🔲 SANDBOX scope for shared templates
- 🔲 **Provider-agnostic storage**
  - 🔲 Memory provider for development
  - 🔲 Filesystem provider for local deployments
  - 🔲 S3 provider for production cloud
  - 🔲 SQLite provider for embedded/desktop
- 🔲 **Checkpoint system integration**
  - 🔲 Project versioning with checkpoints
  - 🔲 Render versioning with checkpoints
  - 🔲 Restore from checkpoint functionality

### Phase 4: Advanced Features 🔮 FUTURE
- 🔲 **Custom theme builder**
  - 🔲 Visual theme editor
  - 🔲 Theme versioning with checkpoints
  - 🔲 Theme templates as SANDBOX namespaces
- 🔲 **Animation timeline editor**
  - 🔲 Visual timeline editing
  - 🔲 Real-time preview
- 🔲 **Audio sync**
  - 🔲 Audio file support
  - 🔲 Beat detection and sync
- 🔲 **Asset management**
  - 🔲 Media assets via chuk-artifacts BLOB namespaces
  - 🔲 Metadata-based asset search and discovery
  - 🔲 Batch asset operations (upload, tag, organize)
  - 🔲 Asset collections and libraries
  - 🔲 Image/video/audio asset support
  - 🔲 Asset versioning with checkpoints
- 🔲 **Auto-captioning**
  - 🔲 Speech-to-text integration
  - 🔲 Caption overlays
  - 🔲 Store captions as artifacts
- 🔲 **Light/dark mode switching**
  - 🔲 Theme variants
  - 🔲 Dynamic mode switching

### Phase 5: Multi-tenancy & Production 🔮 FUTURE
- 🔲 **Multi-tenant architecture**
  - 🔲 User authentication and authorization
  - 🔲 User-scoped project isolation
  - 🔲 Quota management per user
- 🔲 **Production deployment**
  - 🔲 S3 backend for cloud storage
  - 🔲 Redis session management
  - 🔲 Distributed rendering
  - 🔲 CDN integration for renders
- 🔲 **API and webhooks**
  - 🔲 REST API for project/render management
  - 🔲 Webhook notifications for render completion
  - 🔲 Batch render API

## See Also

- [Themes Guide](themes.md) - Theme system documentation
- [Token System](token-system.md) - Design tokens documentation
- [Virtual Filesystem](virtual-filesystem.md) - VFS integration guide
- [chuk-artifacts](https://github.com/chrishayuk/chuk-artifacts) - Unified artifact storage (external)
