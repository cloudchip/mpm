import os
import json
import subprocess
import argparse

# Constants
REGISTRY_URL = "https://raw.githubusercontent.com/ctpldev/mpm-registry/main/registry.json"
CONFIG_FILE = "platform.json"
LIB_DIR = "lib"
DEV_DIR = "dev"

# Utility Functions
def load_registry():
    """Load the library registry from the remote URL."""
    try:
        import requests
        response = requests.get(REGISTRY_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error loading registry: {e}")
        return {}

def load_config():
    """Load the platform.json configuration file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    """Save the configuration to platform.json."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

# Commands
def init_platform(args):
    """Initialize a new project for a specific platform."""
    platform = args.platform or "gcc"
    config = {
        "name": os.path.basename(os.getcwd()),
        "platform": platform,
        "dependencies": {}
    }
    os.makedirs(DEV_DIR, exist_ok=True)
    os.makedirs(f"{DEV_DIR}/src", exist_ok=True)
    os.makedirs(f"{DEV_DIR}/include", exist_ok=True)
    os.makedirs(LIB_DIR, exist_ok=True)

    # Create a hello world main.c file
    main_c_path = os.path.join(DEV_DIR, "src", "main.c")
    with open(main_c_path, "w") as f:
        f.write(
            """#include <stdio.h>

int main() {
    printf(\"Hello, World!\\n\");
    return 0;
}
"""
        )

    save_config(config)
    print(f"Initialized project for platform: {platform}")

def install_library(args):
    """Install a library by name."""
    registry = load_registry()
    config = load_config()

    if args.library not in registry.get("libraries", {}):
        print(f"Library '{args.library}' not found in registry.")
        return

    library = registry["libraries"][args.library]
    url = library["source"]
    version = library["version"]

    # Clone or update library
    dest_dir = os.path.join(LIB_DIR, args.library)
    if os.path.exists(dest_dir):
        print(f"Library '{args.library}' is already installed.")
    else:
        print(f"Installing library '{args.library}'...")
        subprocess.run(["git", "clone", "--branch", version, url, dest_dir])

    # Update platform.json
    config["dependencies"][args.library] = version
    save_config(config)
    print(f"Library '{args.library}' installed successfully.")

def build_project(args):
    """Build the project using the specified platform."""
    config = load_config()
    platform = config.get("platform", "gcc")
    print(f"Building project for platform: {platform}...")

    # Compile source files
    src_dir = os.path.join(DEV_DIR, "src")
    build_dir = "build"
    os.makedirs(build_dir, exist_ok=True)
    
    source_files = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if f.endswith(".c")]
    if platform == "gcc":
        compile_cmd = ["gcc", "-o", os.path.join(build_dir, "main")] + source_files
        subprocess.run(compile_cmd)
        print("Build complete.")
    else:
        print(f"Platform '{platform}' not supported yet.")

def deploy_project(args):
    """Deploy the compiled binaries to the target device."""
    print("Deploying project...")
    # Deployment logic will depend on the platform and tools used

# Main CLI Handler
def main():
    parser = argparse.ArgumentParser(description="Microcontroller Package Manager (MPM)")
    subparsers = parser.add_subparsers()

    # Init command
    parser_init = subparsers.add_parser("init", help="Initialize a new project")
    parser_init.add_argument("platform", nargs="?", help="Target platform (default: gcc)")
    parser_init.set_defaults(func=init_platform)

    # Install command
    parser_install = subparsers.add_parser("install", help="Install a library")
    parser_install.add_argument("library", help="Library name to install")
    parser_install.set_defaults(func=install_library)

    # Build command
    parser_build = subparsers.add_parser("build", help="Build the project")
    parser_build.set_defaults(func=build_project)

    # Deploy command
    parser_deploy = subparsers.add_parser("deploy", help="Deploy the project")
    parser_deploy.set_defaults(func=deploy_project)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
