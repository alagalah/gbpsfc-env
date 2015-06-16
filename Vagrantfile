
# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  odl=ENV['ODL']
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get -y remove grub-pc
    apt-get -y install grub-pc
    grub-install /dev/sda # precaution
    update-grub 
    apt-get install -f -y > /dev/null
    apt-get clean -y > /dev/null
    apt-get autoclean -y > /dev/null
    apt-get update 
    apt-get -y upgrade
    apt-get install -y software-properties-common > /dev/null
    apt-get install -y python-software-properties > /dev/null
    apt-get install -y git-core git > /dev/null
    apt-get install -y docker.io > /dev/null
    apt-get install -y vim > /dev/null
    ln -sf /usr/bin/docker.io /usr/local/bin/docker
    sed -i '$acomplete -F _docker docker' /etc/bash_completion.d/docker.io
    update-rc.d docker.io defaults
    sudo docker pull ubuntu:14.04
    apt-get install -y curl > /dev/null
    apt-get install -y python-pip
    pip install ipaddr
    echo "export PATH=$PATH:/vagrant" >> /home/vagrant/.profile
    echo "export ODL=#{odl}" >> /home/vagrant/.profile    
    export ODL=#{odl}
    sudo /vagrant/ovsinstall.sh
  SHELL

  num_nodes = (ENV['NUM_NODES'] || 1).to_i

  # ip configuration
  ip_base = (ENV['SUBNET'] || "192.168.50.")
  ips = num_nodes.times.collect { |n| ip_base + "#{n+70}" }

  num_nodes.times do |n|
    config.vm.define "gbpsfc#{n+1}", autostart: true do |compute|
      vm_ip = ips[n]
      vm_index = n+1
      compute.vm.box = "trusty64"
      compute.vm.box_url = "http://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_ubuntu-14.04_chef-provisionerless.box"
      compute.vm.hostname = "gbpsfc#{vm_index}"
      compute.vm.network "private_network", ip: "#{vm_ip}"
      compute.vm.provider :virtualbox do |vb|
        vb.memory = 1024
        vb.customize ["modifyvm", :id, "--ioapic", "on"]      
        vb.cpus = 1
      end
    end
  end
end
