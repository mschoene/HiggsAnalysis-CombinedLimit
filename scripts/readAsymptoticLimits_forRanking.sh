#!bin/bash

dir=$1
Label=$2
Mass1=$3
Mass2=$4
#dir='T1tttt'

massString=${Mass1}_${Mass2}

if [[ $Mass2 == -1 ]]
then
massString=${Mass1}
fi


for i in $(ls ${dir}/splitRegions_${massString}/*log)

#dataCards_T2bH_sep27_b012_10unc/splitRegions_450_300/splitCard_HT0toInf_j0_b0toInf_pT0.txt  

#Model=$1

#for i in $(ls ranking_${Model}/log_${Model}*Paper*post*)
do
    if [[ $i ]]
    then

#	echo $i
	region=${i##*splitCard_}
#	region=${i##*splitCard_HT0toInf_}
#	echo $region
	region=${region%.txt.log*}
#	echo $region

	limit=$(grep "50.0%" $i | awk '{print $5}')
	obslimit=$(grep "Observed" $i | awk '{print $5}')

	if [[ $limit ]]
	then
          #  yield=$(grep rate /scratch/`whoami`/datacards_${Model}/datacard_${region}_m*_${Model}.txt | awk '{ sum+=$2} END {print sum}')
          #  bkg=$(grep rate /scratch/`whoami`/datacards_${Model}/datacard_${region}_m*_${Model}.txt | awk '{ sum+=$3+$4+$5} END {print sum}')
	    echo $region $limit $obslimit >> ${dir}/AsymptoticRanking_${Label}_${massString}.txt

            #  echo $region $limit $obslimit $yield $bkg>> AsymptoticRanking_${Model}_Paper_post.txt
	    #echo $region >> AsymptoticRanking_${Model}_Paper_post_plusBG.txt
	    # for d in $(ls -rt /scratch/`whoami`/datacards_${Model}/datacard_${region}_m*)
	    # do
	    # 	bin=${d##*${region}_}
	    # 	bin=${bin%_${Model}.txt}
	    # 	thisyield=$(grep rate /scratch/`whoami`/datacards_${Model}/datacard_${region}_${bin}_${Model}.txt | awk '{ sum=$2} END {print sum}')
	    # 	thisbkg=$(grep rate /scratch/`whoami`/datacards_${Model}/datacard_${region}_${bin}_${Model}.txt | awk '{ sum=$3+$4+$5} END {print sum}')
	    # 	echo $bin '&' $thisyield '&' $thisbkg '\\'>>AsymptoticRanking_${Model}_Paper_post_plusBG.txt
	    # done

	fi
    fi
done

#echo `rm -f log_${Model}*ANvApril*`