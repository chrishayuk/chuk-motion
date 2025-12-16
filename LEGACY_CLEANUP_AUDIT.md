# Legacy Code Cleanup Audit

**Date:** November 30, 2025
**Status:** 🚧 IN PROGRESS

---

## 🎯 Goal

Ensure 100% migration to chuk-artifacts with zero legacy filesystem-based operations and no `run_in_executor` usage for async-native code.

---

## 📋 Findings

### ✅ Good News

1. **AsyncProjectManager in place** - `src/chuk_motion/utils/async_project_manager.py` exists and is functional
2. **Artifact storage active** - Using chuk-artifacts for all persistence
3. **Server aliasing** - `project_manager = async_project_manager` (line 63 of server.py)
4. **No legacy imports** - Legacy ProjectManager not imported anywhere
5. **remotion_create_project migrated** - Already using async_project_manager

### ❌ Issues Found

#### 1. Legacy ProjectManager File Still Exists
- **File:** `src/chuk_motion/utils/project_manager.py` (27,618 bytes)
- **Action:** Should be deleted
- **Risk:** Low (not imported, but confusing)

#### 2. run_in_executor Usage (11 occurrences)
These defeat the async-native architecture:

| Line | Function | Uses project_manager? | Action Needed |
|------|----------|----------------------|---------------|
| 123  | `remotion_list_components` | ❌ No | **Keep** (component registry is sync) |
| 167  | `remotion_search_components` | ❌ No | **Keep** (component search is sync) |
| 195  | `remotion_get_component_schema` | ❌ No | **Keep** (schema lookup is sync) |
| 360  | `remotion_generate_video` | ✅ Yes | **REMOVE** - make fully async |
| 385  | `remotion_get_composition_info` | ✅ Yes | **REMOVE** - make fully async |
| 404  | `remotion_list_projects` | ✅ Yes | **REMOVE** - make fully async |
| 453  | `remotion_add_track` | ✅ Yes | **REMOVE** - make fully async |
| 476  | `remotion_list_tracks` | ✅ Yes | **REMOVE** - make fully async |
| 505  | `remotion_set_active_track` | ✅ Yes | **REMOVE** - make fully async |
| 541  | `remotion_get_track_cursor` | ✅ Yes | **REMOVE** - make fully async |
| 579  | `remotion_get_info` | ✅ Yes | **REMOVE** - make fully async |

**Summary:**
- 3 should keep executor (component registry operations)
- 8 should be converted to direct async calls

#### 3. Filesystem Operations

**Legitimate (Rendering):**
- `artifact_tools.py:40` - VFS export for Remotion CLI (✅ OK)
- `artifact_tools.py:444` - Temp directory for rendering (✅ OK)

**No other filesystem operations found** ✅

#### 4. Documentation References

Files with outdated docstrings mentioning ProjectManager:
- `src/chuk_motion/tools/token_tools.py:27`
- `src/chuk_motion/tools/theme_tools.py:24`
- `src/chuk_motion/components/__init__.py:158`

**Action:** Update docstrings to mention AsyncProjectManager

---

## 🔧 Cleanup Plan

### Phase 1: Remove run_in_executor for Project Operations

Convert these 8 functions to direct async calls:

1. **remotion_generate_video** (line 275-360)
   - Remove `def _generate():` wrapper
   - Make all calls direct to `await async_project_manager.*`
   - Async methods exist: `add_component_to_project`, `generate_composition`

2. **remotion_get_composition_info** (line 364-385)
   - Direct access to `async_project_manager.current_composition`
   - Already async-safe

3. **remotion_list_projects** (line 389-404)
   - Check if `list_projects()` method exists in AsyncProjectManager
   - If not, implement it using artifact storage

4. **remotion_add_track** (line 413-453)
   - Direct access to `async_project_manager.current_timeline.add_track()`
   - Already async-safe

5. **remotion_list_tracks** (line 457-476)
   - Direct access to `async_project_manager.current_timeline.list_tracks()`
   - Already async-safe

6. **remotion_set_active_track** (line 480-505)
   - Direct access to `async_project_manager.current_timeline.set_active_track()`
   - Already async-safe

7. **remotion_get_track_cursor** (line 509-541)
   - Direct access to `async_project_manager.current_timeline.get_track_cursor()`
   - Already async-safe

8. **remotion_get_info** (line 550-579)
   - May need to implement in AsyncProjectManager
   - Or use `get_project()` from artifact storage

### Phase 2: Delete Legacy Files

```bash
rm src/chuk_motion/utils/project_manager.py
```

### Phase 3: Update Documentation

Update docstrings in:
- `src/chuk_motion/tools/token_tools.py`
- `src/chuk_motion/tools/theme_tools.py`
- `src/chuk_motion/components/__init__.py`

---

## ⚠️ Important Notes

1. **Timeline is in-memory** - `current_timeline` is a Timeline object stored in AsyncProjectManager, not persisted to VFS yet
2. **Component generation** - Uses AsyncProjectManager methods which write to VFS
3. **Composition generation** - Should write to VFS not local filesystem

---

## ✅ Validation Checklist

After cleanup:
- [ ] Zero `run_in_executor` calls for async_project_manager operations
- [ ] Zero direct filesystem operations outside temp rendering
- [ ] Legacy project_manager.py deleted
- [ ] All docstrings updated
- [ ] All tests passing
- [ ] No `run_in_executor` except for:
  - Component registry lookups (sync operations)
  - Any genuinely CPU-bound operations

---

## 🎯 Expected Outcome

- **100% async-native** - No `run_in_executor` for VFS/artifact operations
- **100% artifact storage** - All persistence through chuk-artifacts
- **Zero legacy code** - project_manager.py removed
- **Clean architecture** - Async all the way down

---

## 📝 Implementation Priority

**HIGH:** Remove run_in_executor for project operations (breaks async benefits)
**MEDIUM:** Delete legacy project_manager.py (causes confusion)
**LOW:** Update docstrings (cosmetic)
