

COMMUNE_DIR=~/commune
COMMUNE_EXISTS=$(ls -d $COMMUNE_DIR 2>/dev/null)

if [ -d "$COMMUNE_DIR" ]; then
  echo "Commune already exists at $COMMUNE_DIR"
  echo "Please remove it before running this script"

else
    git clone https://github.com/commune-ai/commune.git $COMMUNE_DIR 
    pip install -e $COMMUNE_DIR
fi

pip install communex
pip install bittensor
