@echo off
REM ---------------------------------------------------------------------------
REM Launch Blender 5.1 forcing the OpenGL GPU backend.
REM
REM Blender 5.1 defaults to Vulkan on Windows; on old Intel integrated-graphics
REM drivers Vulkan hangs forever on "Compiling shaders". OpenGL avoids that.
REM
REM Usage:
REM   * Double-click this file  -> opens an empty Blender (then File > Open a station)
REM   * Drag a .blend onto this file -> opens that station directly
REM ---------------------------------------------------------------------------
"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" --gpu-backend opengl %*
