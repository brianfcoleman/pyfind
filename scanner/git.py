from subprocess import Popen, PIPE


def scan(repo_path):
    command = ['git', 'ls-files']
    process = Popen(command, stdout=PIPE, universal_newlines=True)
    process.wait()
    if process.returncode == 0:
        for line in process.stdout:
            yield normalize_path(join(repo_path, line.strip()))



