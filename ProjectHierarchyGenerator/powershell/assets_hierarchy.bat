@echo off

:: Define condition and custom paths variables
set CONDITION="Assets"
set "PS_SCRIPT=C:\SITE\PRODPIPELINETOOLS\other_tool_dev\ProjectHierarchyGenerator\powershell\process_hierarchy.ps1"

:: Run the PowerShell script and pass the condition
powershell -NoProfile -ExecutionPolicy Bypass -File "%PS_SCRIPT%" -Condition "%CONDITION%"
pause