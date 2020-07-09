RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

printf "\n\n\n"
printf "####################\n"
printf "# PACKAGE INSTALL  #\n"
printf "####################\n\n"
python3 setup.py install
setup_ret=$?

if [[ 0 != ${setup_ret} ]] ; then
    echo -e "${RED}Setup: FAIL${NC}"
    exit ${setup_ret}
else
    echo -e "${GREEN}Setup: PASS${NC}"
fi