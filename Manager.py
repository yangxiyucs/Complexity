from flask import Flask, request, jsonify
from time import time
from pygit2 import Repository, clone_repository

app = Flask(__name__)

# pulls repo from url and stores clone
def set_repo():
    try:
        repo = Repository('./repo')
    except:
        repo_url = 'https://github.com/rubik/radon.git'
        repo_path = './repo'
        repo = clone_repository(repo_url, repo_path)
    return repo

# find Out all the commits and store it
def get_commits(repo):
    commits = []
    for commit in repo.walk(repo.head.target):
        commits.append(repo.get(commit.id))
    return commits

# give work to any worker who access the url
@app.route('/work' , methods=['GET'])
def give_work():
    repo = set_repo()
    commits = get_commits(repo)
    global next_task

    try:
        commit_hash = commits[next_task]
        next_task += 1
        if next_task == 350:
            end_time = time() - start_time
            print(end_time)
            # print(result_list) # prints the result list containing the cyclomatic complexity of the py files in the commits
        return jsonify({'commit': str(commit_hash.id), 'id': next_task})
    except:
        return None

# store results that are sent to this url
@app.route('/results', methods=['POST'])
def store_result():
    result = request.json
    result_list.append(result)
    return 'Submission is Received'

if __name__ == '__main__':
    next_task = 0
    start_time = time()
    global result_list
    result_list = []
    app.run(threaded=True, debug=True)
