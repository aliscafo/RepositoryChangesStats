import sys
from github import Github
from collections import Counter
from tabulate import tabulate
from urllib.request import urlopen

num_commits = 50
repository_name = None
repo = None

def get_last_commits(name, username=None, password=None):
    global repo
    g = None
    if username is None:
        g = Github()
    else:
        g = Github(username, password)
    repo = g.get_repo(name)
    return repo.get_commits()[:num_commits]

def save_changes(commits):
    global repo
    for commit in commits:
        file = open(repository_name.replace("/", ".") + "-sha=" + commit.sha, "wb")
        diff_url = repo.compare(commit.parents[0].sha, commit.sha)
        f = urlopen(diff_url.diff_url)
        content = f.read()
        file.write(content)
        file.close()

def list_authors(commits):
    counter = Counter()
    for commit in commits:
        counter[commit.author.login] += 1
    print(tabulate(counter.most_common(), headers=["Username", "Commits"]))

def small_and_big_commits_authors(commits):
    biggest_commit = None
    biggest_commit_size = 0
    smallest_commit = None
    smallest_commit_size = float("inf")

    for commit in commits:
        if commit.stats.total > biggest_commit_size:
            biggest_commit = commit
            biggest_commit_size = commit.stats.total
        if commit.stats.total < smallest_commit_size:
            smallest_commit = commit
            smallest_commit_size = commit.stats.total

    print(
        "The biggest commit author: " + biggest_commit.author.login + " (" +
        biggest_commit.sha + ", " + str(biggest_commit_size) + " changes)")
    print(
        "The smallest commit author: " + smallest_commit.author.login + " (" +
        smallest_commit.sha + ", " + str(smallest_commit_size) + " changes)")

def list_files_by_changes(commits):
    counter = Counter()
    for commit in commits:
        for file in commit.files:
            counter[file.filename] += 1

    print(tabulate(counter.most_common(), headers=["Filename", "Changes"]))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        repository_name = sys.argv[1]
        last_commits = None
        if len(sys.argv) > 3:
            last_commits = get_last_commits(repository_name, sys.argv[2], sys.argv[3])
        else:
            print("Consider authorization, cause for unauthenticated requests, the rate limit allows "
                  "for up to 60 GitHub API requests per hour "
                  "(example: python3 changes_stats.py googledatalab/datalab <username> <password>)")
            last_commits = get_last_commits(repository_name)

        save_changes(last_commits)
        print("Info:\n")
        list_authors(last_commits)
        print()
        small_and_big_commits_authors(last_commits)
        print()
        list_files_by_changes(last_commits)
    else:
        print("Repository name must be specified (example: python3 changes_stats.py googledatalab/datalab)")
