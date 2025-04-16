import os
import shutil
import argparse

def get_file_category_and_extension(file_path):
    """Determine the category and subfolder based on file extension."""
    filename = os.path.basename(file_path)
    file_extension = os.path.splitext(filename)[1].lower()
    
    # Remove the dot from extension for folder naming
    extension_folder = file_extension[1:] if file_extension.startswith('.') else file_extension
    
    # Images
    if file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg']:
        return "Images", extension_folder
    
    # Videos
    elif file_extension in ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.3gp']:
        return "Videos", extension_folder
    
    # Audio
    elif file_extension in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a']:
        return "Audio", extension_folder
    
    # Documents
    elif file_extension in ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx']:
        return "Documents", extension_folder
    
    # Code
    elif file_extension in ['.py', '.java', '.c', '.cpp', '.h', '.js', '.html', '.css', '.php', '.rb', '.go', '.ts', '.json']:
        return "Code", extension_folder
    
    # Archives
    elif file_extension in ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2']:
        return "Archives", extension_folder
    
    # Executables
    elif file_extension in ['.exe', '.msi', '.app', '.bat', '.sh', '.dmg']:
        return "Executables", extension_folder
    
    # Default case
    return "Others", extension_folder or "unknown"

def organize_files(source_dir, destination_dir=None, action='move', recursive=False):
    """
    Organize files from source directory into hierarchical folders:
    Category folders (Documents, Images, etc.) with extension subfolders (.pdf, .jpg, etc.)
    
    Parameters:
    - source_dir: Directory containing files to organize
    - destination_dir: Where to create category folders (defaults to source_dir/Organized)
    - action: 'move' to relocate files, 'copy' to duplicate them
    - recursive: Whether to process subdirectories
    """
    # Validate source directory
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' doesn't exist.")
        return False
    
    # Set destination directory if not specified
    if destination_dir is None:
        destination_dir = os.path.join(source_dir, "Organized")
    
    # Create destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    # Statistics for reporting
    stats = {
        "processed": 0,
        "skipped": 0,
        "categories": {},
        "extensions": {}
    }
    
    # Function to process a single file
    def process_file(file_path):
        try:
            # Skip the destination directory itself
            if os.path.abspath(file_path).startswith(os.path.abspath(destination_dir)):
                return
                
            # Get file details
            filename = os.path.basename(file_path)
            
            # Determine category and extension subfolder
            category, extension_folder = get_file_category_and_extension(file_path)
            
            # Create category folder if it doesn't exist
            category_path = os.path.join(destination_dir, category)
            if not os.path.exists(category_path):
                os.makedirs(category_path)
            
            # Create extension subfolder if it doesn't exist
            extension_path = os.path.join(category_path, extension_folder)
            if not os.path.exists(extension_path):
                os.makedirs(extension_path)
            
            # Prepare target path
            target_path = os.path.join(extension_path, filename)
            
            # Handle name conflicts
            if os.path.exists(target_path):
                base_name, extension = os.path.splitext(filename)
                counter = 1
                while os.path.exists(target_path):
                    new_filename = f"{base_name}_{counter}{extension}"
                    target_path = os.path.join(extension_path, new_filename)
                    counter += 1
            
            # Move or copy the file
            if action == 'move':
                shutil.move(file_path, target_path)
            else:  # copy
                shutil.copy2(file_path, target_path)
            
            # Update statistics
            stats["processed"] += 1
            
            # Update category statistics
            if category in stats["categories"]:
                stats["categories"][category] += 1
            else:
                stats["categories"][category] = 1
                
            # Update extension statistics
            if extension_folder in stats["extensions"]:
                stats["extensions"][extension_folder] += 1
            else:
                stats["extensions"][extension_folder] = 1
                
            print(f"{action.capitalize()}d: {filename} → {category}/{extension_folder}")
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            stats["skipped"] += 1
    
    # Walk through the directory structure
    if recursive:
        for root, _, files in os.walk(source_dir):
            for filename in files:
                file_path = os.path.join(root, filename)
                process_file(file_path)
    else:
        # Process only files in the top-level directory
        for item in os.listdir(source_dir):
            file_path = os.path.join(source_dir, item)
            if os.path.isfile(file_path):
                process_file(file_path)
    
    # Print summary
    print("\n--- Summary ---")
    print(f"Files {action}d: {stats['processed']}")
    print(f"Files skipped: {stats['skipped']}")
    
    print("\nCategories:")
    for category, count in stats["categories"].items():
        print(f"  - {category}: {count} files")
    
    print("\nExtensions:")
    for extension, count in stats["extensions"].items():
        print(f"  - {extension}: {count} files")
    
    return True

def main():
    # Check if args were provided
    if len(sys.argv) > 1:
        # Set up command-line argument parsing
        parser = argparse.ArgumentParser(description="Organize files into hierarchical folders by category and extension.")
        parser.add_argument("source_dir", help="Directory containing files to organize")
        parser.add_argument("-d", "--dest", help="Destination directory (default: source_dir/Organized)")
        parser.add_argument("-a", "--action", choices=["move", "copy"], default="move",
                            help="Action to perform on files (move or copy)")
        parser.add_argument("-r", "--recursive", action="store_true", 
                            help="Process subdirectories recursively")
        
        args = parser.parse_args()
        
        print(f"\nHierarchical File Organizer")
        print(f"{'=' * 50}")
        print(f"Source directory: {args.source_dir}")
        print(f"Destination: {'<source>/Organized' if args.dest is None else args.dest}")
        print(f"Action: {args.action} files")
        print(f"Recursive: {'Yes' if args.recursive else 'No'}")
        print(f"{'=' * 50}\n")
        
        # Confirm before proceeding
        response = input("Proceed with organization? (y/n): ").strip().lower()
        if response != 'y':
            print("Operation cancelled.")
            return
        
        # Call the organize function with arguments
        organize_files(
            args.source_dir,
            args.dest,
            args.action,
            args.recursive
        )
    else:
        # Use current directory when run without arguments
        current_dir = os.getcwd()
        print(f"\nHierarchical File Organizer")
        print(f"{'=' * 50}")
        print(f"No arguments provided. Using default settings:")
        print(f"Source directory: {current_dir}")
        print(f"Destination: {current_dir}/Organized")
        print(f"Action: move files")
        print(f"Recursive: No")
        print(f"{'=' * 50}\n")
        
        # Confirm before proceeding
        response = input("Proceed with organization? (y/n): ").strip().lower()
        if response != 'y':
            print("Operation cancelled.")
            return
            
        # Call organize_files with default parameters
        organize_files(current_dir)

if __name__ == "__main__":
    import sys  # Add this import at the top
    main()