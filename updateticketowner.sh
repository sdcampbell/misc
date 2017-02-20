if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
	echo "Usage: updateticketowner.sh <input file with ticket numbers> <qualys user id>"
	exit 1
fi

ticketowner=$2
counter=0

while read line; do
    ticknum=${line%$'\r'}
	curl -u username:password -H 'X-Requested-With:QualysApiExplorer' "https://qualysapi.qualys.com:443/msp/ticket_edit.php?ticket_numbers=${ticknum}&change_assignee=${ticketowner}" > /dev/null
	counter=$((counter+1))
	echo "Tickets Updated: $counter"
done < $1
