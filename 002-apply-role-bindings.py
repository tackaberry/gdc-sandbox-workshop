#!/usr/bin/env python3
import yaml
import subprocess
import os
import sys


def main():
    """
    Main function to apply IAM role bindings to projects based on a config file.
    """
    print("🚀 Starting application of IAM Role Bindings...")
    print("-------------------------------------------------")

    # Construct the path to the config file, assuming it's in the same directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "projects_config.yaml")

    try:
        with open(config_path, "r", encoding="utf-8") as stream:
            data = yaml.safe_load(stream)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {config_path}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML file: {exc}", file=sys.stderr)
        sys.exit(1)

    projects = data.get("projects")
    role_sets = data.get("roleSets")

    if not projects or not role_sets:
        print("Error: 'projects' or 'roleSets' not found in the config file.", file=sys.stderr)
        sys.exit(1)

    for project in projects:
        project_name = project.get("name")
        org_id = project.get("orgId")
        users = project.get("users")

        if not project_name or not users:
            continue

        print(f"Processing project: '{project_name}'")

        for user_spec in users:
            user_email = user_spec.get("user")
            role_set_ref = user_spec.get("roleSetRef")

            if not user_email or not role_set_ref or not role_set_ref.startswith("roleSets/"):
                continue

            role_set_name = role_set_ref.split('/')[-1]
            roles_to_apply = role_sets.get(role_set_name, {}).get("roles", [])

            if not roles_to_apply:
                print(f"  - Warning: Role set '{role_set_name}' not found or has no roles.")
                continue

            print(f"  - Applying roles for user '{user_email}'...")
            for role in roles_to_apply:
                command = [
                    "gdcloud", "projects", "add-iam-policy-binding", project_name,
                    f"--member=user:{user_email}",
                    f"--role={role}"
                ]
                result = subprocess.run(command, capture_output=True, text=True, check=False)

                if result.returncode == 0:
                    print(f"    - Successfully applied role '{role}'.")
                else:
                    print(f"    - Failed to apply role '{role}'. Error: {result.stderr.strip()}")

            # if org_id is provided, also apply org roles
            if org_id:
                org_roles_to_apply = role_sets.get(role_set_name, {}).get("orgRoles", [])
                print(f"  - Applying org roles for user '{user_email}'...")
                for role in org_roles_to_apply:
                    command = [
                        "gdcloud", "organizations", "add-iam-policy-binding", org_id,
                        f"--member=user:{user_email}",
                        f"--role={role}"
                    ]
                    result = subprocess.run(command, capture_output=True, text=True, check=False)

                    if result.returncode == 0:
                        print(f"    - Successfully applied role '{role}'.")
                    else:
                        print(f"    - Failed to apply role '{role}'. Error: {result.stderr.strip()}")

if __name__ == "__main__":
    main()