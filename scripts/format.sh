if [[ ! -d "./oresat_helmholtz" ]] || [[ ! -d "./test" ]]
then
  echo Must run from top-level source directory.
  exit 1
fi

for cmd in black isort
do
  which $cmd
  if [[ $? -ne 0 ]]
  then
    echo Required tool \'$cmd\' not found.
    echo Please see the readme for installation instructions.
    exit 1
  fi
done

echo
echo Formatting
echo
black ./test
black ./oresat_helmholtz

echo
echo Sorting includes
echo
isort ./test
isort ./oresat_helmholtz
