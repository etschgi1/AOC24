import os

def setup_environment():
    # Get the current script directory
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Loop through folder names from 01 to 24
    for i in range(1, 25):
        folder_name = f"{i:02}"  # Format as two digits, e.g., 01, 02, etc.
        folder_path = os.path.join(base_path, folder_name)
        
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
            # Create input.txt if it doesn't exist
            input_file = os.path.join(folder_path, "input.txt")
            if not os.path.exists(input_file):
                with open(input_file, "w") as f:
                    pass  # Create an empty file
            
            # Create XX.py if it doesn't exist
            script_file = os.path.join(folder_path, f"{folder_name}.py")
            if not os.path.exists(script_file):
                with open(script_file, "w") as f:
                    # Write the script content
                    f.write(f"""
    def read_data(chdir=True):
        if chdir:
            import os
            os.chdir(os.path.dirname(__file__))
        with open('input.txt') as f:
            lines = f.readlines()
        return lines

    if __name__ == "__main__":
        lines = read_data()
    """)

if __name__ == "__main__":
    setup_environment()
    print("Environment setup complete!")
