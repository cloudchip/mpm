import os
import json
import subprocess
import argparse
import platform as sys_platform

# Constants
REGISTRY_URL = "https://raw.githubusercontent.com/your-username/mpm-registry/main/registry.json"
CONFIG_FILE = "platform.json"
LIB_DIR = "lib"
DEV_DIR = "dev"
OBJ_DIR = "output/obj"
BIN_DIR = "output/bin"

# Determine the compiler based on the OS
def get_compiler():
    current_os = sys_platform.system()
    if current_os == "Windows":
        return "mingw32-gcc"
    elif current_os == "Linux":
        return "gcc"
    elif current_os == "Darwin":  # macOS
        return "gcc"
    else:
        raise Exception(f"Unsupported OS: {current_os}")

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

def create_makefile(platform):
    """Generate a Makefile for the project."""
    makefile_content = f"""
CC := {platform}
SRC := $(wildcard {DEV_DIR}/src/*.c)
OBJ := $(patsubst {DEV_DIR}/src/%.c, {OBJ_DIR}/%.o, $(SRC))
INCLUDE := -I{DEV_DIR}/include
LIBS := -L{LIB_DIR} -l$(notdir $(basename $(wildcard {LIB_DIR}/*)))
OUT := {BIN_DIR}/main

all: $(OUT)

$(OUT): $(OBJ)
	$(CC) $(OBJ) $(LIBS) -o $(OUT)

{OBJ_DIR}/%.o: {DEV_DIR}/src/%.c
	@mkdir -p $(OBJ_DIR)
	$(CC) -c $< $(INCLUDE) -o $@

clean:
	rm -rf {OBJ_DIR}/* {BIN_DIR}/*
"""
    with open("Makefile", "w") as f:
        f.write(makefile_content)

# Commands
def init_platform(args):
    """Initialize a new project for a specific platform."""
    project_name = args.project_name
    platform = args.platform or get_compiler()
    config = {
        "name": project_name,
        "platform": platform,
        "dependencies": {}
    }

    # Create project folder
    os.makedirs(project_name, exist_ok=True)
    os.chdir(project_name)

    # Create required directories
    os.makedirs(DEV_DIR, exist_ok=True)
    os.makedirs(f"{DEV_DIR}/src", exist_ok=True)
    os.makedirs(f"{DEV_DIR}/include", exist_ok=True)
    os.makedirs(LIB_DIR, exist_ok=True)
    os.makedirs(OBJ_DIR, exist_ok=True)
    os.makedirs(BIN_DIR, exist_ok=True)

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

    create_makefile(platform)
    save_config(config)
    print(f"Initialized project '{project_name}' for platform: {platform}")

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
    platform = config.get("platform", get_compiler())
    print(f"Building project for platform: {platform}...")

    # Invoke the Makefile
    subprocess.run(["make"])
    print("Build complete.")

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
    parser_init.add_argument("project_name", help="Name of the project folder to create")
    parser_init.add_argument("--platform", help="Target platform (default: gcc/mingw32-gcc)")
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
