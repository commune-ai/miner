
if [ -f .env ]; then
    source .env
fi
# IS DOCKER INSTALLED
IS_DOCKER_INSTALLED=$(docker -v)


if [ -z "$IS_DOCKER_INSTALLED" ]; then
    echo "DOCKER: INSTALLING"
    if [ -z "$IF_MAC" ]; then
        sudo apt-get update
        sudo apt-get install docker
    else
        brew install docker
    fi

    # Verify that Docker has been installed correctly
    groupadd docker
    usermod -aG docker $USER
    chmod 666 /var/run/docker.sock
    
else
    echo "DOCKER: INSTALLED"
fi

