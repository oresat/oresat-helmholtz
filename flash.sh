target_dir="/run/media/$USER/CIRCUITPY"

GREEN='\e[0;32m'
BLUE='\e[0;34m'
NC='\e[0m' # No Color (reset)

for file in "./"*.py; do
  if [ $file = "./main.py" ]; then
     location="$target_dir"
  else
    location="$target_dir/lib"
  fi
  echo -e "Flashing $BLUE$file$NC to $BLUE$location$NC"
  cp $file $location 
done

echo "Syncing..."
sync # Linux must sync to actually write the files

echo -e "${GREEN}Done${NC}"
