#!/usr/bin/env bash
#!/bin/bash -   
#title          :.sh    
#description    :packme 
#author         :jho       
#date           :20210609
#usage          :./.sh  
#notes          :       
#bash_version   :4.4.19(1)-release
#git 
#============================================================================




mydir=$PWD
echo $mydir
mypath=`git rev-parse --show-toplevel` 
mybase=`basename $mypath`

function logme {
	mystr=`echo $1 |tr ' ' '¤'`
	printf "`date`: %s\n"  $mystr  |tr '¤' ' '
}


function clean {
rm -fr ${mypath}/packages
}

function create_clean_pip {
	rm -fr ${mypath}/venv
	python3 -m venv venv >/dev/null 2>&1
	source venv/bin/activate >/dev/null 2>&1
	pip install --upgrade pip >/dev/null 2>&1
	pip install requests
	pip install requirements-parser
	pip freeze > $mypath/cleanpip.txt >/dev/null 2>&1

}

function pip_addons {
      pip install django-debug-toolbar
      pip install sphinx sphinxcontrib-autoprogram
      pip install awxkit
      }



cd $mypath
if [[ $? == 0 ]];
then
	logme "Ready to pack" 	
else
	logme "We are not where we are supposed to be"
fi


logme "Cleaning"
clean
logme "Create clean venv for build process"
create_clean_pip

logme "Fetch packages"
cd $mypath/parser &&  ./fetch_specific_packages.py
pip_addons



exit
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



