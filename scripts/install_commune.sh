
REPO=commune-ai/commune
if [ -f .env ]; then
    source .env
fi
LIB_NAME=$(echo $REPO | cut -d'/' -f2)
REPO_PATH=$HOME/$LIB_NAME

 if [ ! -d "$REPO_PATH" ]; then
     echo "$LIB_NAME: CLONING"
     GITHUB_REPO=https://github.com/$REPO.git
     git clone $GITHUB_REPO $REPO_PATH
fi

# if the libname is not installed in the python environment, install it
if ! python3 -c "import $LIB_NAME" &> /dev/null; then
    echo "$LIB_NAME: INSTALLING"
    python3 -m pip install -e $REPO_PATH --break-system-packages
else
    echo "$LIB_NAME: INSTALLED"
fi




