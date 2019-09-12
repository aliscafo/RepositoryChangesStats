# RepositoryChangesStats

RepositoryChangesStats application takes the last 50 commits from the specified repository, saves changes into files (per commit) and prints some stats: a list of authors sorted by the number of commits, an author of the largest and smallest in terms of the number of changed commit lines and a list of files sorted by how often they changed. Uses GitHub API (via PyGithub library) to make requests to https://api.github.com.


## Usage

```bash
$ python3 changes_stats.py <repository_name> <username> <password>
```

## Examples

```bash
$ python3 changes_stats.py tensorflow/tensorflow
```

```bash
$ python3 changes_stats.py tensorflow/tensorflow bob 123456789
```

## Requirements
Works well with Python 3.6.

Install [PyGithub](https://github.com/PyGithub/PyGithub)
```bash
$ pip3 install PyGithub
```

Install [tabulate lib](https://pypi.org/project/tabulate/)
```bash
$ pip3 install tabulate
```
