import gi
import requests
import subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

GITLAB_URL = "https://gitlab.com"


"""
A class called `GitLabCloner` that represents a GUI window for cloning GitLab projects. 
It provides a user interface for entering a GitLab access token, a group name, and selecting projects to clone. 
The class has methods for retrieving projects from the GitLab API, displaying them in a tree view, and cloning selected projects to a specified directory.
The class uses the `requests` library to interact with the GitLab API and the `subprocess` module to execute the `git clone` command.
"""


class GitLabCloner(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="GitLab Cloner")
        self.set_border_width(10)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.token_entry = Gtk.Entry()
        self.token_entry.set_placeholder_text("Enter Token")
        vbox.pack_start(self.token_entry, False, False, 0)

        self.group_entry = Gtk.Entry()
        self.group_entry.set_placeholder_text("Enter Group Name")
        vbox.pack_start(self.group_entry, False, False, 0)

        self.check_button = Gtk.Button(label="Vérifier")
        self.check_button.connect("clicked", self.on_check_clicked)
        vbox.pack_start(self.check_button, False, False, 0)

        # Add select all button
        self.select_all_button = Gtk.Button(label="Select All")
        self.select_all_button.connect("clicked", self.on_select_all_clicked)
        vbox.pack_start(self.select_all_button, False, False, 0)

        # Define the TreeView for multiple project selection
        self.projects_store = Gtk.ListStore(bool, str, str)
        self.tree_view = Gtk.TreeView(model=self.projects_store)

        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_toggled)
        column_toggle = Gtk.TreeViewColumn("Select", renderer_toggle, active=0)
        self.tree_view.append_column(column_toggle)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Projects", renderer_text, text=1)
        self.tree_view.append_column(column_text)

        vbox.pack_start(self.tree_view, True, True, 0)

        self.dir_chooser = Gtk.FileChooserButton(
            title="Select a Folder", action=Gtk.FileChooserAction.SELECT_FOLDER
        )
        vbox.pack_start(self.dir_chooser, False, False, 0)

        self.clone_button = Gtk.Button(label="Clone")
        self.clone_button.connect("clicked", self.on_clone_clicked)
        vbox.pack_start(self.clone_button, False, False, 0)

        self.progress_bar = Gtk.ProgressBar()
        vbox.pack_start(self.progress_bar, False, False, 0)

    def on_cell_toggled(self, widget, path):
        self.projects_store[path][0] = not self.projects_store[path][0]

    def on_check_clicked(self, widget):
        token = self.token_entry.get_text()
        group_name = self.group_entry.get_text()
        projects = self.get_projects(token, group_name)

        # Update TreeView with projects
        self.projects_store.clear()
        for project in projects:
            self.projects_store.append([False, project[0], project[1]])

    def get_projects(self, token, group_name):
        group_id = self.get_group_id(token, group_name)
        if group_id:
            return self.get_projects_from_group(token, group_id)
        return []

    def get_group_id(self, token, group_name):
        headers = {"PRIVATE-TOKEN": token}
        response = requests.get(
            f"{GITLAB_URL}/api/v4/groups?search={group_name}", headers=headers
        )
        if response.status_code == 200 and response.json():
            return response.json()[0]["id"]
        return None

    def get_projects_from_group(self, token, group_id):
        headers = {"PRIVATE-TOKEN": token}
        response = requests.get(
            f"{GITLAB_URL}/api/v4/groups/{group_id}/projects?per_page=100",
            headers=headers,
        )
        if response.status_code == 200:
            projects = response.json()
            return [
                (project["name"], project["ssh_url_to_repo"]) for project in projects
            ]
        return []

    def on_clone_clicked(self, widget):
        clone_dir = self.dir_chooser.get_filename()

        total_projects = sum(1 for row in self.projects_store if row[0])
        cloned_projects = 0

        for row in self.projects_store:
            is_selected, project_name, project_url = row
            if is_selected:
                self.clone_project(project_url, clone_dir)
                cloned_projects += 1
                fraction = cloned_projects / total_projects
                self.progress_bar.set_fraction(fraction)
                while Gtk.events_pending():
                    Gtk.main_iteration_do(False)

    def on_select_all_clicked(self, widget):
        for row in self.projects_store:
            row[0] = True

    def clone_project(self, project_url, clone_dir):
        project_name = project_url.split("/")[-1].replace(".git", "")
        full_clone_path = f"{clone_dir}/{project_name}"
        try:
            subprocess.run(["git", "clone", project_url, full_clone_path], check=True)
        except subprocess.CalledProcessError:
            pass  # Handle the error as appropriate for your application


win = GitLabCloner()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
