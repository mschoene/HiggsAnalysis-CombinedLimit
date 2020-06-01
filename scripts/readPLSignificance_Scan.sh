#!bin/bash

### EXAMPLE (HOW TO RUN):
### sh readPLSignificance_Scan.sh T1tttt 2p3ifb_13Apr_sigContOK

dir=$1
Label=$2
#dir='T1tttt'

for i in $(ls ${dir}/*${Label}*siglog)
#for i in $(ls /scratch/`whoami`/limits_${dir}_${Label}/*txt)
do
    if [[ $i ]]
    then

	echo $i
	mass=${i##*${dir}}
	mass=${mass##*/Datacard_13TeV_${Label}}

	if [[ $Label == "SMS_T2bH_mSbottom" ]]
	then
	    mass=${mass%.txt.siglog*}
	    mass2=${mass##*_mLSP}
	    mass=${mass%*_mLSP*}
	    mass=$mass" "$mass2
	fi

	if [[ $Label == "SMS_TChiWH_HToGG" ]]
	then
	    mass=${mass%*.txt.siglog*}
	    mass2=${mass##*_m}
	    mass=${mass%*_m*}
	    mass=${mass##*_m}
	    mass=$mass" "$mass2
	fi

	if [[ $Label = "SMS_TChiHH_HToGG"  || $Label = "SMS_TChiHZ_HToGG"  ]]; then
	    #HH and HZ
	    mass=${mass%.txt.siglog*}
	    mass=${mass##*_m}
	fi
	
#	echo $mass
#       echo $i
#	mass=${i##*log_${Model}_}
#	mass=${mass%_combined.txt*}
	echo $mass

	significance=$(grep "Significance" $i | awk '{print $2}')
	pvalue=$(grep "p-value" $i | awk '{print $3}')
	if [[ $significance ]]
	then
	echo $mass $significance $pvalue  >> ${dir}/significance_${Label}.txt
	search="_"
	replace=" "
	sed -i "s/$search/$replace/g" ${dir}/significance_${Label}.txt
	search=")"
	replace=""
	sed -i "s/$search/$replace/g" ${dir}/significance_${Label}.txt



	fi
    fi
done

