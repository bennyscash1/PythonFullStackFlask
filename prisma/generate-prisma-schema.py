import os
import shutil
import subprocess
import sys

def copy_and_modify_schema(source_file, destination_dir):
    # Check if the source file exists
    if not os.path.exists(source_file):
        print(f"Error: Source file does not exist: {source_file}", file=sys.stderr)
        sys.exit(1)

    # Check if the destination directory exists
    if not os.path.exists(destination_dir):
        print(f"Error: Destination directory does not exist: {destination_dir}", file=sys.stderr)
        print("Please create the directory manually or check the path.", file=sys.stderr)
        sys.exit(1)

    # Set up file paths
    destination_file = os.path.join(destination_dir, "schema.prisma")

    try:
        # Copy the schema file
        shutil.copy2(source_file, destination_file)

        # Read the content of the copied file
        with open(destination_file, 'r') as file:
            content = file.read()

        # Modify the generator section
        content = content.replace('provider        = "prisma-client-js"', 'provider = "prisma-client-py"')
        content = content.replace('previewFeatures = ["driverAdapters"]', 'interface = "asyncio"\n  recursive_type_depth = 5')

        # Write the modified content back to the file
        with open(destination_file, 'w') as file:
            file.write(content)

        print(f"schema.prisma has been successfully copied and modified at {destination_file}")
    except Exception as e:
        print(f"Error: Failed to copy or modify schema.prisma. {str(e)}", file=sys.stderr)
        sys.exit(1)

def generate_prisma_client(destination_dir):
    # Run Prisma generate
    try:
        os.chdir(destination_dir)
        subprocess.run(["prisma", "generate"], check=True)
        print("Prisma client has been regenerated")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to generate Prisma client. {str(e)}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Warning: Prisma command not found. Skipping client generation.", file=sys.stderr)


if __name__ == "__main__":
  # Get user input for source directory
    source_file = input("Enter the absolute path to the source schema.prisma: ").strip()

   # Use relative path for the destination directory
    dest_dir = os.path.dirname(os.path.abspath(__file__))

    copy_and_modify_schema(source_file, dest_dir)
    generate_prisma_client(dest_dir)
