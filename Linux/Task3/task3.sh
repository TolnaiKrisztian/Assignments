#!/bin/bash
source config.cfg

for i in "${YEARS[@]}"; do
psql -h $HOSTNAME -U $USERNAME $DATABASE --csv << EOF >> invoices_"$i".csv
$QUERY $YEAR $i $ORDER
EOF
gzip invoices_"$i".csv
done

mv *.csv.gz $WDIRECTORY
