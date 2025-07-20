# This file provides instructions on how to create a virtual environment for cogs18 projects that will contain all of the necessary packages.
# Run the following line to open the terminal window, or press ctrl + ` (backtick) to open the terminal in VS Code.
print('Use the terminal to create a virtual environment for this cogs18 project.')


# Type the following command in the terminal to create a virtual environment named 'cogs18venv':
# Note: You can replace 'cogs18venv' with any name you prefer for
# python -m venv cogs18venv
# Select "Yes" when promtted about associating the virtual environment with the current workspace.

# After creating the virtual environment, you need to activate it.
# Kill the termianal and run this script again to activate the virtual environment.

#If you get an error about not being able to run scripts, you may run the follwowing command in PowerShell administrator mode:
# Set-ExecutionPolicy RemoteSigned
# Type "A" for "Yes to All" when prompted.
# Kill the terminal and run this script again to activate the virtual environment.

# Install the following packages in the virtual environment:
# pip install numpy

# If you are getting an error when installing numpy, you may need to install Microsoft C++ Build Tools.
# You can download it from https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Use python 3.11 and pyinstaller to create an executable file for your project.