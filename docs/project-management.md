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

## See Also

- [Themes Guide](themes.md) - Theme system documentation
- [Token System](token-system.md) - Design tokens documentation
- [Virtual Filesystem](virtual-filesystem.md) - VFS integration guide
