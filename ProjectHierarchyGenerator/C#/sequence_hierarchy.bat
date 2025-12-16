@echo off
echo Running ProcessHierarchy for Sequence...
set "EXE_PATH=C:/SITE/ProdPipelineTools/other_tool_dev/ProjectHierarchyGenerator/C#/process_hierarchy/bin/Debug/net9.0/process_hierarchy.exe"

IF NOT EXIST "%EXE_PATH%" (
    ECHO Error: The executable was not found at "%EXE_PATH%"
    PAUSE
    EXIT /B
)

echo Running: "%EXE_PATH%" Sequence
CALL "%EXE_PATH%" Sequence

pause