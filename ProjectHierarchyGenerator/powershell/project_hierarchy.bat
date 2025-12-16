@echo off

:: Define condition and custom paths variables
set CONDITION="Main"
set "PS_SCRIPT=C:\SITE\PRODPIPELINETOOLS\other_tool_dev\ProjectHierarchyGenerator\powershell\process_hierarchy.ps1"

:: Run PowerShell script to create folders and copy files
powershell -NoProfile -ExecutionPolicy Bypass -File "%PS_SCRIPT%" -Condition "%CONDITION%"
pause