# -*- coding: utf-8 -*_

import json
from subprocess import *
from pathlib import Path

import dotfav


test_temp = Path(__file__).parent / 'temp'
home = test_temp / 'home'
dotfiles = test_temp / 'dotfiles'
dotfiles_home = dotfiles / 'home'
dotfiles_config = dotfiles / 'dotfav.config'


def create_test_temp_directories():
    test_temp.mkdir()
    home.mkdir()
    dotfiles.mkdir()
    dotfiles_home.mkdir()


def create_config_file(config):
    config = json.loads(config)
    with dotfiles_config.open(mode='w') as f:
        json.dump(config, f)


def run_dotfav(command, dotfiles, home, platform=None):
    cmd = ['python', '-m', 'dotfav', command, '--dotfiles', dotfiles, '--home', home]
    if platform is not None:
        cmd.extend(['--platform', platform])

    with Popen(cmd, stdout=PIPE, stderr=PIPE) as process:
        try:
            output, error = process.communicate()
        except:
            process.kill()
            process.wait()
            raise
        retcode = process.poll()
        if retcode:
            raise CalledProcessError(retcode, process.args, output=output)
