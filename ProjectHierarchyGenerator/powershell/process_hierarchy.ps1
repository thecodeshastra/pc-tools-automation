param (
    [string]$Condition = "Main"  # Default value if no argument is passed
)

$projectRoot = "C:\SITE\PRODPIPELINETOOLS\other_tool_dev\ProjectHierarchyGenerator"

# Define JSON file paths based on the condition
if ($Condition -eq "Main") {
    $JSON_FILE = $projectRoot + "\project_hierarchy.json"
} elseif ($Condition -eq "Assets") {
    $JSON_FILE =  $projectRoot + "\assets_hierarchy.json"
} elseif ($Condition -eq "Shots") {
    $JSON_FILE =  $projectRoot + "\shots_hierarchy.json"
} elseif ($Condition -eq "Sequence") {
    $JSON_FILE =  $projectRoot + "\sequence_hierarchy.json"
} else {
    Write-Host "Error: No matching condition found!"
    exit 1
}

# Check if the JSON file exists
if (-Not (Test-Path $JSON_FILE)) {
    Write-Host "Error: JSON file not found - $JSON_FILE"
    exit 1
}

# Read JSON File
$jsonData = Get-Content $JSON_FILE | ConvertFrom-Json

# Function to create folders recursively
function Create_Folders {
    param ($parentPath, $folderData)

    # Set folder path
    # Use 'name' instead of 'root' for subfolders
    $folderName = $folderData.name
    $folderPath = Join-Path -Path $parentPath -ChildPath $folderName

    # create the folder
    New-Item -Path $folderPath -ItemType Directory -Force | Out-Null
    Write-Host "Created: $folderPath"
 
    # Copy files if defined
    if ($folderData.PSObject.Properties["copy_files"]) {
        foreach ($file in $folderData.copy_files) {
            # Replace "$PROJECT_ROOT$" with actual project path
            $new_projectRoot = $projectRoot + "\powershell"
            $filePath = $file -replace "PROJECT_ROOT", $new_projectRoot
            if (Test-Path $filePath) {
                Copy-Item -Path $filePath -Destination $folderPath -Force
                Write-Host "Copied: $filePath to $folderPath"
            } else {
                Write-Host "File not found: $filePath"
            }
        }
    }

    # Check if "subfolders" is a string (external JSON reference)
    if ($folderData.PSObject.Properties["subfolders"] -and $folderData.subfolders -is [string]) {
        $externalJsonFile = $folderData.subfolders
        $externalJsonFile = $externalJsonFile -replace "PROJECT_ROOT", $projectRoot
        if (Test-Path $externalJsonFile) {
            $externalSubfolders = Get-Content $externalJsonFile | ConvertFrom-Json
            foreach ($subfolder in $externalSubfolders) {
                Create_Folders -parentPath $folderPath -folderData $subfolder
            }
        } else {
            Write-Host "Warning: External JSON file not found: $externalJsonFile"
        }
    }
    # Process regular subfolders
    elseif ($folderData.PSObject.Properties["subfolders"]) {
        foreach ($subfolder in $folderData.subfolders) {
            Create_Folders -parentPath $folderPath -folderData $subfolder
        }
    }
}
# Start from the current directory
Create_Folders -parentPath (Get-Location) -folderData $jsonData