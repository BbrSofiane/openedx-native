# Fresh installations of Ubuntu do not have a locale yet, and this will cause
# the Open edX installer scripts to fail, so we'll  set it now.
# For any input prompts that follow, you can select the default value.
# locale-gen sets the character set for terminal output.
locale-gen en_GB en_GB.UTF-8

# With the locale set, we'll reconfigure the Ubuntu packages
# to use whatever character set you selected.
# dpkg-reconfigure locales
dpkg --configure -a

# Update Ubuntu 16.04   
apt-get update
apt-get upgrade -y
apt-get install -y awscli

# Create config.yml
cd ~ 

export PUBLIC_IP=$(curl ifconfig.me)
echo -e "EDXAPP_LMS_BASE: \"$PUBLIC_IP\"\nEDXAPP_CMS_BASE: \"$PUBLIC_IP:18010\"" > config.yml

# Install open edX
wget https://raw.githubusercontent.com/BbrSofiane/edx.scripts/master/edx.platform-install.sh
chmod +x edx.platform-install.sh
sudo nohup ./edx.platform-install.sh &

#export OPENEDX_RELEASE=open-release/juniper.master

# 2. Bootstrap the Ansible installation:
#wget https://raw.githubusercontent.com/edx/configuration/$OPENEDX_RELEASE/util/install/ansible-bootstrap.sh -O - | sudo -H bash

# 3. (Optional) If this is a new installation, randomize the passwords:
#if test ! -f "my-passwords.yml"; then
#    wget https://raw.githubusercontent.com/edx/configuration/$OPENEDX_RELEASE/util/install/generate-passwords.sh -O - | bash
#fi
# 4. Install Open edX:
#wget https://raw.githubusercontent.com/edx/configuration/$OPENEDX_RELEASE/util/install/native.sh -O - | bash > install.out