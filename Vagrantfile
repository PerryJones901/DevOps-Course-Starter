# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "hashicorp/bionic64"
  config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    sudo apt-get update

    # Install pyenv prerequisites
    sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

    # Install pyenv
    ## 1. Clone Repo
      git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    ## 2. Define Env Vars
      echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
      echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
      echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
    ## 3. Adding pyenv init to shell
      source ~/.bash_profile

    # Install Python 3.8.2 and set as global
    pyenv install 3.8.2
    pyenv global 3.8.2

    # Install Poetry
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
  SHELL

  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the TODO app setup script"
    trigger.run_remote = { privileged: false, inline: "
      cd /vagrant
      poetry install
      poetry run gunicorn -w 4 'app:create_app()' --bind 0.0.0.0:5000 --daemon --access-logfile gunicorn.log
    " }
  end
end

# # To run using flask:
# poetry run flask run --host 0.0.0.0
