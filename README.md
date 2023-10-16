# GitLab Cloner

GitLab Cloner is a simple GUI application that facilitates the process of cloning multiple repositories from a specific GitLab group. Simply provide your personal access token, specify the group name, and select the projects you wish to clone.

## Features

- **Token and Group Input**: Simply enter your GitLab personal access token and the name of the group containing the repositories you want to clone.
- **Project Selection**: Once the group's projects are listed, you can select multiple projects to clone.
- **Select All Button**: With just one click, select all the projects listed.
- **Clone Progress**: A progress bar displays the cloning progress, updating after each repository is cloned.

## Requirements

- Python
- GTK+ 3
- Requests library

## Installation

1. Ensure you have Python and GTK+ 3 installed on your system.
2. Install the required Python libraries:
   ```bash
   pip install requests PyGObject
3. Install complements
 ```bash
   sudo apt-get install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0 
   
1. Clone this repository:
   ```bash
   git clone https://github.com/AoNovae/Git-Toolkit.git
2. Navigate to the repository
    ```bash
    cd Git-Toolkit
3. Activate env
   ```bash
   python3 -m venv .venv --system-site-packages
   . .venv/bin/activate
   pip install -r requirements.txt

## Usage

1. Run the script:
    ```bash
    python clone_all.py
2. Enter your GitLab personal access token in the "Enter Token" field.
3. Enter the desired group name in the "Enter Group Name" field.
4. Click "Check" to fetch and display the projects in that group.
5. Select the projects you wish to clone (or use the "Select All" button to select all projects).
6. Choose the directory where the projects should be cloned.
7. Click "Clone" to start the cloning process. The progress bar will update as each repository is cloned.


## Licence 

This project is open source. Feel free to use, modify, and distribute as you see fit.

