"""This script prepares a tool by copying source files, building Cython modules, 
and cleaning up Python files.
It also copies extra files like LICENSE, README.md, and JSON files to the deployment directory.
It is designed to be run in a specific project structure and can be customized for different tools.
"""

import os
import shutil
from pathlib import Path
from argparse import ArgumentParser
from setuptools import Extension, setup
from Cython.Build import cythonize


def clean_deploy_dir(deploy_base_dir: Path):
    """Clean all contents of deploy_base_dir, but not the folder itself.
    
    Args:
        deploy_base_dir (Path): The directory to clean.
    """
    for item in deploy_base_dir.iterdir():
        if item.is_dir():
            shutil.rmtree(item, ignore_errors=True)
        else:
            try:
                item.unlink()
            except Exception as ex:
                print(f"Warning: Could not delete {item}: {ex}")


def copy_src_to_deploy(src_dir: Path, deploy_tool_dir: Path):
    """Copy source files from the source directory to the deployment directory.
    
    Args:
        src_dir (Path): The source directory containing the tool's source files.
        deploy_tool_dir (Path): The deployment directory where files will be copied.
    """
    deploy_tool_dir.mkdir(parents=True, exist_ok=True)
    # Copy contents of src_dir into deploy_tool_dir
    for item in src_dir.iterdir():
        dest = deploy_tool_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)


def build_cython_modules(deploy_tool_dir: Path):
    """Build Cython modules from Python files in the deployment directory.
    
    Args:
        deploy_tool_dir (Path): The directory containing Python files to compile.
    """
    py_files = [str(p) for p in deploy_tool_dir.rglob("*.py")]
    if not py_files:
        print("No Python files to compile.")
        return
    # Prepare the Cython extensions
    ext_modules = cythonize(
        [Extension("*", [p]) for p in py_files],
        compiler_directives={"language_level": "3"},
        build_dir="build_temp"
    )
    # Setup the build process
    setup(
        script_name='setup.py',  # script_name needed for some envs
        name="cy_build",
        ext_modules=ext_modules,
        script_args=["build_ext", "--inplace"],
        options={"build_ext": {"build_lib": str(deploy_tool_dir)}},
    )


def cleanup_py_files(deploy_tool_dir: Path):
    """Remove all Python source files from the deployment directory.
    
    Args:
        deploy_tool_dir (Path): The directory from which to remove Python files.
    """
    for py_file in deploy_tool_dir.rglob("*.py"):
        try:
            py_file.unlink()
        except Exception as ex:
            print(f"Warning: Could not delete {py_file}: {ex}")


def copy_extra_files(base_path: Path, deploy_path: Path):
    """Copy extra files like LICENSE, README.md, and JSON files to the deployment directory.

    Args:
        base_path (Path): The base directory containing the files to copy.
        deploy_path (Path): The deployment directory where files will be copied.
    """
    for file in base_path.iterdir():
        if (
            file.is_file() and (
                file.name.lower() == "readme.md"
                or file.name.upper().startswith("LICENSE")
                or file.suffix.lower() == ".json"
            )
        ):
            shutil.copy2(file, deploy_path / file.name)


def prepare_tool_with_cython(base_dir: str, tool_name: str):
    """Prepare the tool by copying source files, building Cython modules,
    and cleaning up Python files.

    Args:
        base_dir (str): The base directory of the tool project.
        tool_name (str): The name of the tool, used for the deployment subfolder.
    """
    base_path = Path(base_dir).resolve()
    src_path = base_path / "src"
    deploy_base = base_path / "deploy"
    deploy_tool_path = deploy_base / tool_name

    print(f"🧹 Cleaning deploy directory: {deploy_base}")
    clean_deploy_dir(deploy_base)

    print(f"🛠️ Copying source files to: {deploy_tool_path}")
    copy_src_to_deploy(src_path, deploy_tool_path)

    print("📄 Copying LICENSE, README.md, and JSON files...")
    copy_extra_files(base_path, deploy_base)

    print("🔐 Building encrypted .pyd files with Cython...")
    orig_dir = os.getcwd()
    try:
        os.chdir(deploy_tool_path)
        build_cython_modules(deploy_tool_path)
    finally:
        os.chdir(orig_dir)

    print("🧹 Cleaning up .py source files...")
    cleanup_py_files(deploy_tool_path)

    print(f"✅ Done! Encrypted tool is ready at: {deploy_tool_path}")


def main():
    """Main function to parse arguments and prepare the tool."""
    parser = ArgumentParser(
        description="Prepare a tool with Cython encryption."
    )
    parser.add_argument(
        "-bd",
        "--base_dir",
        required=True,
        type=str,
        help="Path to the base directory of the tool project."
    )
    parser.add_argument(
        "-tn",
        "--tool_name",
        required=True,
        type=str,
        help="Name of the tool (for deploy subfolder)."
    )
    args = parser.parse_args()
    prepare_tool_with_cython(args.base_dir, args.tool_name)


# Example entrypoint
if __name__ == "__main__":
    main()
