#!/usr/bin/env bash
mydir=$PWD

for DIR in `ls -l packages|grep drw|awk '{ print $9 }' `
do
	RAW=`ls -l ${PWD}/packages/${DIR}|grep $DIR |grep drwx 2>&1`
	if [[ $? ==  0 ]];
	then 
		printf "%-40s dir is ok\n" $DIR
		#echo $RAW
	else
		printf "%-40s dir is in error\n" $DIR
		DIR2=`echo $DIR |tr '-' '_'`
		DIROK=`echo $DIR |tr '_' '-'`
		RAW=`ls -l ${PWD}/packages/${DIR}|grep -i $DIR2 |grep drw`
		if [[ $? == 0 ]];
		then
			SRC=`echo $RAW |awk '{ print $9 }'`
			DST=`echo $SRC |tr '_' '-' |tr '[A-Z]' '[a-z]' `

			mv ${PWD}/packages/$DIR/$SRC ${PWD}/packages/${DIR}/${DST}
		fi

	fi
done



