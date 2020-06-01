#!bin/bash

### EXAMPLE (HOW TO RUN):
### sh readAsymptoticLimits_Scan.sh T1tttt 2p3ifb_13Apr_sigContOK

dir=$1
Label=$2
#dir='T1tttt'

for i in $(ls ${dir}/*${Label}*logging)
#for i in $(ls /scratch/`whoami`/limits_${dir}_${Label}/*txt)
do
    if [[ $i ]]
    then

	echo $i
	mass=${i##*${dir}}
	mass=${mass##*/Datacard_13TeV_${Label}}

	if [[ $Label == "SMS_T2bH_mSbottom" ]]
	then
	    mass=${mass%.txt.logging*}
	    mass2=${mass##*_mLSP}
	    mass=${mass%*_mLSP*}
	    mass=$mass" "$mass2
	fi

	if [[ $Label == "SMS_TChiWH_HToGG" ]]
	then
	    mass=${mass%*.txt.logging*}
	    mass2=${mass##*_m}
	    mass=${mass%*_m*}
	    mass=${mass##*_m}
	    mass=$mass" "$mass2
	fi

	if [[ $Label = "SMS_TChiHH_HToGG"  || $Label = "SMS_TChiHZ_HToGG"  ]]; then
	    #HH and HZ
	    mass=${mass%.txt.logging*}
	    mass=${mass##*_m}
	fi
	
	echo $mass

	limit=$(grep "50.0%" $i | awk '{print $5}')
	limit_ps=$(grep "84.0%" $i | awk '{print $5}')
	limit_ms=$(grep "16.0%" $i | awk '{print $5}')
	limit_p2s=$(grep "97.5%" $i | awk '{print $5}')
	limit_m2s=$(grep "2.5%" $i | awk '{print $5}')
	limit_obs=$(grep "Observed" $i | awk '{print $5}')
	if [[ $limit ]]
	then
#	    echo $mass $limit $limit_obs $limit_ps $limit_ms $limit_p2s $limit_m2s  
	    echo $mass $limit $limit_obs $limit_ps $limit_ms $limit_p2s $limit_m2s  >> ${dir}/limits_${Label}.txt
	    search="_"
	    replace=" "
	    sed -i "s/$search/$replace/g" ${dir}/limits_${Label}.txt #limits_${dir}_${Label}.txt
	    echo " "

	fi
    fi
done

#for i in $(ls /scratch/mmasciov/limits_T1tttt_2p3ifb_13Apr_sigContOK/*txt)
#do
#    if [[ $i ]]
#    then
#	#echo $i
#	mass=${i##*log_${dir}_}
#	mass=${mass%_2p3ifb.txt*}
#	echo $mass
#	limit=$(grep "50.0%" $i | awk '{print $5}')
#	limit_ps=$(grep "84.0%" $i | awk '{print $5}')
#	limit_ms=$(grep "16.0%" $i | awk '{print $5}')
#	limit_p2s=$(grep "97.5%" $i | awk '{print $5}')
#	limit_m2s=$(grep "2.5%" $i | awk '{print $5}')
#	limit_obs=$(grep "Observed" $i | awk '{print $5}')
#	if [[ $limit ]]
#	then
#	echo $mass $limit $limit_obs $limit_ps $limit_ms $limit_p2s $limit_m2s  >> limits_${dir}_full_13Apr_sigContOK.txt
#	search="_"
#	replace=" "
#	sed -i "s/$search/$replace/g" limits_${Model}_full_13Apr_sigContOK.txt
#	fi
#    fi
#done
