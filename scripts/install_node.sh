if [ -f .env ]; then
    source .env
fi
IF_MAC=$(uname -a | grep Darwin)
IS_NODE_INSTALLED=$(node -v)
if [ -z "$IS_NODE_INSTALLED" ]; then
    echo "NODE: INSTALLING"
    if [ -z "$IF_MAC" ]; then
        sudo apt-get update
        sudo apt-get install nodejs
    else
        brew install node
    fi
else
    echo "NODE: INSTALLED"
fi

IS_NPM_INSTALLED=$(npm -v)

if [ -z "$IS_NPM_INSTALLED" ]; then
    echo "NPM: INSTALLING"
    if [ -z "$IF_MAC" ]; then
        sudo apt-get update
        sudo apt-get install npm
    else
        brew install npm
    fi
else
    echo "NPM: INSTALLED"
fi

IS_PM2_INSTALLED=$(pm2 -v)
if [ -z "$IS_PM2_INSTALLED" ]; then
    echo "PM2: INSTALLING"
    npm install pm2 -g
else
    echo "PM2: INSTALLED"
fi
