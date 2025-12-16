using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;

class Folder
{
    public string name { get; set; } = string.Empty;
    public object subfolders { get; set; } = new List<object>(); // Can be a List or a String (JSON Path)
    public List<string> copy_files { get; set; } = new List<string>();
}

class Program
{
    static string projectRoot = "C:/SITE/ProdPipelineTools/other_tool_dev/ProjectHierarchyGenerator"; // Define project root here

    static void Main(string[] args)
    {
         if (args.Length == 0)
        {
            Console.WriteLine("Error: No arguments received.");
            return;
        }
        if (args.Length < 1)
        {
            Console.WriteLine("Usage: process_hierarchy <Condition>");
            return;
        }
        Console.WriteLine($"Received argument: {args[0]}");
        string condition = args[0];

        string jsonFilePath = ReplaceProjectRoot(condition switch
        {
            "Main" => "PROJECT_ROOT/project_hierarchy.json",
            "Assets" => "PROJECT_ROOT/assets_hierarchy.json",
            "Shots" => "PROJECT_ROOT/shots_hierarchy.json",
            "Sequence" => "PROJECT_ROOT/sequence_hierarchy.json",
            _ => throw new Exception("Error: No matching condition found!")
        });

        if (!File.Exists(jsonFilePath))
        {
            Console.WriteLine($"Error: JSON file '{jsonFilePath}' not found.");
            return;
        }

        string batFileDirectory = GetBatFileDirectory();
        if (string.IsNullOrEmpty(batFileDirectory))
        {
            Console.WriteLine("Error: Unable to determine .bat file location.");
            return;
        }

        string jsonContent = File.ReadAllText(jsonFilePath);
        Folder? rootFolder;

        try
        {
            rootFolder = JsonSerializer.Deserialize<Folder>(jsonContent);
            if (rootFolder == null)
            {
                throw new JsonException("Deserialized JSON is null.");
            }
        }
        catch (JsonException ex)
        {
            Console.WriteLine($"Error: Invalid JSON format - {ex.Message}");
            return;
        }

        string rootPath = Path.Combine(batFileDirectory, rootFolder.name);
        Directory.CreateDirectory(rootPath);
        Console.WriteLine($"Created: {rootPath}");

        // Process file copying inside the correct folder
        CopyFiles(rootFolder.copy_files, rootPath);

        ProcessSubfolders(rootPath, rootFolder.subfolders);
    }

    static void ProcessSubfolders(string parentPath, object subfolderData)
    {
        if (subfolderData is JsonElement jsonElement)
        {
            if (jsonElement.ValueKind == JsonValueKind.String)
            {
                string jsonPath = ReplaceProjectRoot(jsonElement.GetString()!);

                if (File.Exists(jsonPath))
                {
                    string jsonContent = File.ReadAllText(jsonPath);
                    try
                    {
                        Folder? subFolderRoot = JsonSerializer.Deserialize<Folder>(jsonContent);
                        if (subFolderRoot != null)
                        {
                            string subfolderRootPath = Path.Combine(parentPath, subFolderRoot.name);
                            Directory.CreateDirectory(subfolderRootPath);
                            Console.WriteLine($"Created: {subfolderRootPath}");

                            // Process file copying inside the correct folder
                            CopyFiles(subFolderRoot.copy_files, subfolderRootPath);

                            ProcessSubfolders(subfolderRootPath, subFolderRoot.subfolders);
                        }
                    }
                    catch (JsonException ex)
                    {
                        Console.WriteLine($"Error: Invalid JSON format in '{jsonPath}' - {ex.Message}");
                    }
                }
                else
                {
                    Console.WriteLine($"Warning: JSON file '{jsonPath}' not found, skipping...");
                }
                return;
            }
            else if (jsonElement.ValueKind == JsonValueKind.Array)
            {
                List<object>? subfolders = JsonSerializer.Deserialize<List<object>>(jsonElement.GetRawText());
                if (subfolders != null)
                {
                    foreach (var item in subfolders)
                    {
                        ProcessSingleSubfolder(parentPath, item);
                    }
                }
            }
        }
    }

    static void ProcessSingleSubfolder(string parentPath, object item)
    {
        if (item is JsonElement subfolderElement && subfolderElement.ValueKind == JsonValueKind.Object)
        {
            try
            {
                Folder subfolder = subfolderElement.Deserialize<Folder>()!;
                string subfolderPath = Path.Combine(parentPath, subfolder.name);
                Directory.CreateDirectory(subfolderPath);
                Console.WriteLine($"Created: {subfolderPath}");

                // Process file copying inside the correct folder
                CopyFiles(subfolder.copy_files, subfolderPath);

                ProcessSubfolders(subfolderPath, subfolder.subfolders);
            }
            catch (JsonException ex)
            {
                Console.WriteLine($"Error: Failed to parse subfolder object - {ex.Message}");
            }
        }
    }

    static void CopyFiles(List<string> files, string targetFolder)
    {
        foreach (var file in files)
        {
            string sourceFile = ReplaceProjectRoot(file);
            string destinationFile = Path.Combine(targetFolder, Path.GetFileName(sourceFile));

            if (File.Exists(sourceFile))
            {
                File.Copy(sourceFile, destinationFile, true);
                Console.WriteLine($"Copied: {sourceFile} -> {destinationFile}");
            }
            else
            {
                Console.WriteLine($"Warning: File '{sourceFile}' not found, skipping...");
            }
        }
    }

    static string ReplaceProjectRoot(string path)
    {
        return path.Replace("PROJECT_ROOT", projectRoot);
    }

    static string GetBatFileDirectory()
    {
        return Environment.CurrentDirectory; // Returns the working directory where the .bat file was run
    }
}
