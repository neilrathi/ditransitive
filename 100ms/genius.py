import os

unix_command = "find . -type f -name '*.mp4' ! -name 'Rec*' -exec mv {} . \;"

# Specify the directory where you want to iterate over subdirectories.
base_directory = '/Users/neilrathi/csboy/ditransitive/recordings/run'

# Get a list of subdirectories in the base directory (one layer deep).
subdirectories = [d for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]

for directory in subdirectories:
    full_directory_path = os.path.join(base_directory, directory)
    
    # Use os.chdir() to change the current working directory to the subdirectory.
    os.chdir(full_directory_path)
    
    # Run the Unix command.
    os.system(unix_command)
    
    # Change the current working directory back to the original directory.
    os.chdir('/Users/neilrathi/csboy/ditransitive/recordings/run')