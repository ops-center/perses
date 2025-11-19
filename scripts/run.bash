#!/bin/bash

set -euo pipefail  # Exit on error, unset variables, and pipe failures

FOLDERS=(
#    cassandra ✓
#    connectcluster ✓
#    druid
#    elasticsearch
#    ferretdb
#    hazelcast
#    ignite
#    kafka
#    mariadb
#    memcached
#    mongodb ✓
#    mssqlserver
#    mysql
#    pgbouncer
#    pgpool
    postgres
#    proxysql
#    rabbitmq
#    redis
#    singlestore
#    solr
#    zookeeper

#    falco
#    kubestash
#    kubevault
#    policy
#    scanner
#    stash
)

# Colors for nice output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Starting migration sequence on all top-level folders...${NC}\n"

# Counter for summary
success_count=0
fail_count=0
total_folders=0

for folder in "${FOLDERS[@]}"; do
    total_folders=$((total_folders + 1))

    echo -e "${YELLOW}════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Processing folder: $folder${NC}"
    echo -e "${YELLOW}════════════════════════════════════════════════${NC}"

    fldr=/home/arnob/go/src/go.opscenter.dev/grafana-dashboards/$folder
    echo "$fldr"
    if cd "$fldr" 2>/dev/null; then
        (
            set -e

            echo "0. Running wipeout0.py"
            python3 /home/arnob/go/src/go.opscenter.dev/perses/scripts/wipeout0.py

            echo "1. Running modify1.py"
            python3 /home/arnob/go/src/go.opscenter.dev/perses/scripts/modify1.py

            echo "2. Running curl2.py"
            python3 /home/arnob/go/src/go.opscenter.dev/perses/scripts/curl2.py

            echo "3. Running revert_modify3.py"
            python3 /home/arnob/go/src/go.opscenter.dev/perses/scripts/revert_modify3.py

            echo "4. Running cleanup4.py"
            python3 /home/arnob/go/src/go.opscenter.dev/perses/scripts/cleanup4.py

            echo "5. Running migrate5.py"
            python3 /home/arnob/go/src/go.opscenter.dev/perses/scripts/migrate5.py

            echo "6. Running mappings6.py"
            python3 /home/arnob/go/src/go.opscenter.dev/perses/scripts/mappings6.py

            echo "6. Running widthnull7.py"
            python3 /home/arnob/go/src/go.opscenter.dev/perses/scripts/widthnull7.py

            echo -e "\n${GREEN}✓ All Python scripts completed successfully in $folder${NC}\n"
        )

        if [[ $? -eq 0 ]]; then
            success_count=$((success_count + 1))
        else
            echo -e "${RED}✗ One or more Python scripts failed in $folder${NC}"
            fail_count=$((fail_count + 1))
            cd ..  # Go back even if failed
            continue
        fi

        # Look for any *-migrated.json files in this folder and apply with percli
        shopt -s nullglob
        json_files=( *-migrated.json )
        if ((${#json_files[@]})); then
            echo "Found ${#json_files[@]} migrated JSON files in $folder"
            for jf in "${json_files[@]}"; do
                echo "Applying percli to: $jf"
                percli apply -f "$jf"
            done
            echo -e "${GREEN}✓ percli apply successful for all migrated files in $folder${NC}\n"
        else
            echo -e "${YELLOW}⚠ No *-migrated.json file found in $folder, skipping percli apply${NC}\n"
        fi
        shopt -u nullglob

        cd ..
    else
        echo -e "${RED}Could not enter directory: $folder${NC}"
        fail_count=$((fail_count + 1))
    fi
done

# Final summary
echo -e "${YELLOW}════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Migration sequence completed!${NC}"
echo -e "${YELLOW}Total folders processed: $total_folders${NC}"
echo -e "${GREEN}Successful: $success_count${NC}"
if [[ $fail_count -gt 0 ]]; then
    echo -e "${RED}Failed: $fail_count${NC}"
else
    echo -e "${GREEN}Failed: 0${NC}"
fi
echo -e "${YELLOW}════════════════════════════════════════════════${NC}"
