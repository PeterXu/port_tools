
if [ $# -ne 1 ]; then
	exit 1
fi

file=$1
if [ ! -e $file ]; then
	exit 1
fi

vcard="vcard/iphone_contacts.vcf"
mkdir -p vcard
rm -f $vcard

for LINE in `cat $file`
do
	name2=`echo $LINE | awk -F"," '{print $1}'`
	name1=`echo $LINE | awk -F"," '{print $2}'`
	cell1=`echo $LINE | awk -F"," '{print $3}'`
	cell2=`echo $LINE | awk -F"," '{print $4}'`
	cell3=`echo $LINE | awk -F"," '{print $5}'`
	#echo "nam2: $name2, name1: $name1, cell1: $cell1, cell2: $cell2, cell3: $cell3"
	
	#vcard="vcard/$name1$name2.vcf"
	cat >> $vcard << EOF
BEGIN:VCARD
VERSION:3.0
N:$name1;$name2;;;
FN:$name1$name2
EOF

	if [ "#$cell1" != "#" ]; then
		echo "TEL;TYPE=MAIN;TYPE=pref:$cell1" >> $vcard
	fi
	
	if [ "#$cell2" != "#" ]; then
		echo "TEL;TYPE=CELL;TYPE=VOICE:$cell2" >> $vcard
	fi
	
	if [ "#$cell3" != "#" ]; then
		echo "TEL;TYPE=WORK;TYPE=VOICE:$cell3" >> $vcard
	fi

	cat >> $vcard << EOF
PRODID:-//Apple Inc.//iCloud Web Address Book 14B52//EN
REV:2014-04-12T03:14:08Z
END:VCARD
EOF
	
done  

unix2dos $vcard

exit 0
