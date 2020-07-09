RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

printf "\n\n\n"
printf "############\n"
printf "# LINTING  #\n"
printf "############\n\n"

flake8_msg=$(flake8 pypuzzle3d/ --count --max-line-length=120 --statistics)
flake8_ret=$?

if [[ 0 != ${flake8_ret} ]] ; then
    echo ${flake8_msg}
    echo -e "${RED}Flake8: FAIL${NC}"
    exit ${flake8_ret}
else
    echo -e "${GREEN}Flake8: PASS${NC}"
fi

