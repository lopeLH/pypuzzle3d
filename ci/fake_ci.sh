RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

./ci/setup.sh
setup_ret=$?
./ci/lint.sh
lint_ret=$?
./ci/tests.sh
tests_ret=$?

printf "\n\n"
printf "##################\n"
printf "# CI SUMMARY:    #\n"
printf "##################\n"

if [[ 0 != ${setup_ret} ]] ; then
    echo -e "${RED}Setup: FAIL${NC}"
else
    echo -e "${GREEN}Setup: PASS${NC}"
fi
if [[ 0 != ${lint_ret} ]] ; then
    echo -e "${RED}Flake8: FAIL${NC}"
else
    echo -e "${GREEN}Flake8: PASS${NC}"
fi
if [[ 0 != ${tests_ret} ]] ; then
    echo -e "${RED}Tests: FAIL${NC}"
else
    echo -e "${GREEN}Tests: PASS${NC}"
fi
printf "\n"