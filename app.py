from flask import Flask, render_template, redirect
import subprocess, logging, os, shutil

app = Flask(__name__, static_folder='static/')
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def _git_clone(repository_url, destination_folder):
    """
    Clone a repository.
    """
    try:
        subprocess.run(['git', 'clone', repository_url, destination_folder], check=True)
        logging.info(f"Git clone successful for {repository_url}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Git clone unsuccessful for {repository_url}. Error: {e}")


def _clone_repositories():
    """
    Loop over all repositories in config/repositories.txt and clone them one by one.
    """
    with open('config/repositories.txt', 'r') as f:
        repositories = f.readlines()
    for repository in repositories:
        repository_name = repository.split('/')[-1][:-4].rstrip('.')
        _git_clone(repository.strip(), f'repositories/{repository_name}')


def _buid_docs():
    """
    Run Makefile (currently not working).
    Move documentation to static to be served.
    """
    for folder in os.listdir('repositories'):
        logging.debug(f'Found {folder}.')
        try:
            subprocess.run('documentation/Makefile', shell=True, check=True)
        except Exception as e:
            logging.error(f'Failed on {folder}. {e}')
        
        try:
            if not os.path.exists(f'static/{folder}'):
                os.makedirs(f'static/{folder}')
            shutil.move(f'repositories/{folder}/documentation', f'static/{folder}')
        except Exception as e:
            logging.error(f'Failed to move {folder} to static folder. {e}')
    

def _get_repository_folders():
    repository_path = 'repositories'
    if os.path.exists(repository_path) and os.path.isdir(repository_path):
        return [folder for folder in os.listdir(repository_path) if os.path.isdir(os.path.join(repository_path, folder))]
    else:
        return []
    

@app.route('/')
def hello():
    """
    Render homepage.
    """
    repository_folders = _get_repository_folders()
    return render_template('index.html', repository_folders=repository_folders)


@app.route('/<path:path>')
def serve_sphinx_docs(path='index.html'):
    """
    Serve static path to each repository included in config/repositories.txt
    """
    return app.send_static_file(path)


@app.route('/<folder>')
def repository_page(folder):
    """
    Create a button for each project and reroute to readthedocs of said project.
    """
    documentation_path = os.path.join('static', folder, 'documentation', 'build')
    if os.path.exists(documentation_path):
        html_file_path = os.path.join(documentation_path, 'index.html')
        return redirect(html_file_path)
    else:
        return f"Documentation not found for repository folder: {folder}"

@app.route('/contact')
def contact():
    return render_template('pages/contact.html')

@app.route('/about')
def about():
    return render_template('pages/about.html')

@app.route('/pages/strongholdkingdoms')
def strongholdkingdoms():
    return render_template('pages/strongholdkingdoms.html')

if __name__ == "__main__":
    _clone_repositories()
    _buid_docs()
    app.run(debug=True, host='0.0.0.0', port=5002)
