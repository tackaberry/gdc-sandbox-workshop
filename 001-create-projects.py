#!/usr/bin/env python3
import yaml
import subprocess
import os

def main():

    """
    Main function to onboard projects.
    """
    
    print("🚀 Starting creation of ${#NEW_PROJECT_IDS[@]} GDC Projects...")
    print("--------------------------------------------------------")


    # Construct the path to the config file, assuming it's in the same directory as the script.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "projects_config.yaml")

    with open(config_path, "r", encoding="utf-8") as stream:
        try:
            data = yaml.safe_load(stream)
            if "projects" in data and data["projects"]:
                print("Checking for existing projects...")
                for project in data["projects"]:
                    if "name" in project:
                        project_name = project["name"]
                        command = ["gdcloud", "projects", "describe", project_name]
                        result = subprocess.run(
                            command, capture_output=True, text=True, check=False
                        )

                        if result.returncode == 0:
                            print(f"- Project '{project_name}' already exists.")
                        else:
                            print(f"- Project '{project_name}' does not exist. Creating...")
                            create_command = [
                                "gdcloud",
                                "projects",
                                "create",
                                project_name,
                                "--data-exfiltration-prevention=false",
                            ]
                            create_result = subprocess.run(
                                create_command, capture_output=True, text=True, check=False
                            )
                            if create_result.returncode == 0:
                                print(f"  - Successfully created project '{project_name}'.")
                            else:
                                print(f"  - Failed to create project '{project_name}'.")
                                print(f"    Error: {create_result.stderr.strip()}")
            else:
                print("No projects found under the 'projects' key.")
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML file: {exc}")

if __name__ == "__main__":
    main()