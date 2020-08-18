# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "hashicorp/bionic64"

  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update 
    # TODO: Install pyenv prerequisites
    # TODO: Install pyenv
  SHELL
end
