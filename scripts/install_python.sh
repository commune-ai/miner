if [ -f .env ]; then
    source .env
fi

IF_MAC=$(uname -a | grep Darwin)
IS_PYTHON_INSTALLED=$(python3 -V)

if [ -z "$IS_PYTHON_INSTALLED" ]; then
    echo "PYTHON: INSTALLING"
    if [ -z "$IF_MAC" ]; then
        sudo apt-get update
        sudo apt-get install python3
    else
        brew install python3
    fi
else
    echo "PYTHON: INSTALLED"
fi
