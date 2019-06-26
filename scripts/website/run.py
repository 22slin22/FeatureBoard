import json
import os

from flask import Flask, render_template, request, jsonify, redirect, url_for

from scripts.website.project import Project, ProjectPlayer, project_from_dict

app = Flask(__name__)

projects = []
project_player = None

NUM_PANELS = 3


def get_project_by_name(name):
    """return the project with the given name, if there's no project with this name return None"""
    for project in projects:
        if project.name == name:
            return project
    return None


@app.route('/')
@app.route('/project-selection', methods=['GET', 'POST'])
def project_selection():
    return render_template("project-selection.html", projects=projects)


@app.route('/editor', methods=['POST'])
def editor():
    # project that will be edited
    current_project = None

    if request.method == 'POST':
        result = request.form
        new_project_name = result['project-name']
        # check if there is project with that project name and send it
        if get_project_by_name(new_project_name) is None:
            new_project = Project(new_project_name)
            projects.append(new_project)
            current_project = new_project
        else:
            current_project = get_project_by_name(new_project_name)

    project_names = [project.name for project in projects]
    return render_template("editor.html", project_names=project_names, current_project=current_project.to_dict())


@app.route('/save-project', methods=['POST'])
def save_project():
    data = request.get_json()
    project = get_project_by_name(data['name'])
    project.frames = data['frames']
    project.fps = data['fps']
    save_projects_to_file()
    # send url for a redirect
    return jsonify({"url": "/project-selection"})


@app.route('/play', methods=['POST'])
def play():
    global project_player
    result = request.form
    print("Results:", result)
    project = get_project_by_name(result['project-name'])
    if project is not None:
        if project_player is not None:
            print("Stopping old ProjectPlayer")
            # stop the existing thread
            project_player.stop()
            # wait until the thread has stopped
            project_player.join()
        project_player = ProjectPlayer(project, NUM_PANELS)
        project_player.start()
        print("Started new ProjectPlayer")
    return redirect(url_for('project_selection'))


def load_projects_from_file():
    print("Loading projects from file")
    global projects
    projects = []

    try:
        # check if file is empty
        if os.stat('scripts/website/projects/projects.txt').st_size == 0:
            return
        with open('scripts/website/projects/projects.txt', 'r') as json_projects:
            data = json.load(json_projects)
            for project in data:
                projects.append(project_from_dict(project))
    except FileNotFoundError:
        # there is no projects file -> no project has to be loaded
        pass


def save_projects_to_file():
    """saves all project to a json file"""
    print("Saving project to file")
    with open('scripts/website/projects/projects.txt', 'w') as file:
        project_list = [p.to_dict() for p in projects]
        json.dump(project_list, file)


if __name__ == "__main__":
    load_projects_from_file()
    app.run(host='192.168.2.125', debug=True)
