#!bin/bash

### EXAMPLE (HOW TO RUN):

dir=$1
Label=$2
Mass1=$3
Mass2=$4

#card=${dir}/*${Label}*${Mass1}_${Mass2}.txt
#card=${dir}/*${Label}*${Mass1}_m${Mass2}.txt
card=${dir}/*${Label}*${Mass1}_mLSP${Mass2}.txt
dirOut=${dir}/splitRegions_${Mass1}_${Mass2}

if [[ $Mass2 == -1 ]]
then
    card=${dir}/*${Label}*${Mass1}.txt
    dirOut=${dir}/splitRegions_${Mass1}
fi

mkdir ${dirOut}


#for region in {"diBBZ_pT0","diBBZ_pT1","diBBH_pT0","diBBH_pT1","diLepZ","j0_b0toInf_pT0","j0_b0toInf_pT1","j0_b0toInf_pT2","j0_b0toInf_pT3","j0_b0toInf_pT4","j0_b0toInf_pT5","j0_b0toInf_pT6","j0_b0toInf_pT7","j0_b0toInf_pT8","j0_b0toInf_pT9","is1El_pT0_mt2_0","is1Mu_pT0_mt2_0","is1El_pT0_mt2_30","is1Mu_pT0_mt2_30","is1El_pT1","is1Mu_pT1","j1to3_b0_pT0_mt2_0","j1to3_b0_pT1_mt2_0","j4toInf_b0_pT0_mt2_0","j4toInf_b0_pT1_mt2_0","j1to3_b1_pT0_mt2_0","j1to3_b1_pT1_mt2_0","j4toInf_b1_pT0_mt2_0","j4toInf_b1_pT1_mt2_0","j1to3_b2toInf_pT0_mt2_0","j1to3_b2toInf_pT1_mt2_0","j4toInf_b2toInf_pT0_mt2_0","j4toInf_b2toInf_pT1_mt2_0","j1to3_b0_pT0_mt2_30","j1to3_b0_pT1_mt2_30","j4toInf_b0_pT0_mt2_30","j4toInf_b0_pT1_mt2_30","j1to3_b1_pT0_mt2_30","j1to3_b1_pT1_mt2_30","j4toInf_b1_pT0_mt2_30","j4toInf_b1_pT1_mt2_30","j1to3_b2toInf_pT0_mt2_30","j1to3_b2toInf_pT1_mt2_30","j4toInf_b2toInf_pT0_mt2_30","j4toInf_b2toInf_pT1_mt2_30"}



for region in {"j1to3_b0_pT0_mt2_0","j1to3_b0_pT1_mt2_0","j1to3_b0_pT2_mt2_0","j4toInf_b0_pT0_mt2_0","j4toInf_b0_pT1_mt2_0","j4toInf_b0_pT2_mt2_0","j1to3_b1_pT0_mt2_0","j1to3_b1_pT1_mt2_0","j1to3_b1_pT2_mt2_0","j4toInf_b1_pT0_mt2_0","j4toInf_b1_pT1_mt2_0","j4toInf_b1_pT2_mt2_0","j1to3_b2toInf_pT0_mt2_0","j1to3_b2toInf_pT1_mt2_0","j1to3_b2toInf_pT2_mt2_0","j4toInf_b2toInf_pT0_mt2_0","j4toInf_b2toInf_pT1_mt2_0","j4toInf_b2toInf_pT2_mt2_0","j1to3_b0_pT0_mt2_30","j1to3_b0_pT1_mt2_30","j1to3_b0_pT2_mt2_30","j4toInf_b0_pT0_mt2_30","j4toInf_b0_pT1_mt2_30","j4toInf_b0_pT2_mt2_30","j1to3_b1_pT0_mt2_30","j1to3_b1_pT1_mt2_30","j1to3_b1_pT2_mt2_30","j4toInf_b1_pT0_mt2_30","j4toInf_b1_pT1_mt2_30","j4toInf_b1_pT2_mt2_30","j1to3_b2toInf_pT0_mt2_30","j1to3_b2toInf_pT1_mt2_30","j1to3_b2toInf_pT2_mt2_30","j4toInf_b2toInf_pT0_mt2_30","j4toInf_b2toInf_pT1_mt2_30","j4toInf_b2toInf_pT2_mt2_30","is1El_pT0_mt2_0","is1Mu_pT0_mt2_0","is1El_pT0_mt2_30","is1Mu_pT0_mt2_30","is1El_pT1_mt2_0","is1Mu_pT1_mt2_0","is1El_pT1_mt2_30","is1Mu_pT1_mt2_30","is1El_pT2_mt2_0","is1Mu_pT2_mt2_0","is1El_pT2_mt2_30","is1Mu_pT2_mt2_30","diBBZ_pT0_mt2_0","diBBZ_pT1_mt2_0","diBBZ_pT2_mt2_0","diBBH_pT0_mt2_0","diBBH_pT1_mt2_0","diBBH_pT2_mt2_0","diBBZ_pT0_mt2_30","diBBZ_pT1_mt2_30","diBBZ_pT2_mt2_30","diBBH_pT0_mt2_30","diBBH_pT1_mt2_30","diBBH_pT2_mt2_30","diLepZ","j0_b0toInf_pT0","j0_b0toInf_pT1","j0_b0toInf_pT2"}


do
    echo $card
    echo $region

    if [[ $card ]]
    then
	combineCards.py --ic=.*${region}.* ${card} > ${dirOut}/splitCard_${region}.txt 


	command=`sed -i '/pdfindex/d' ${dirOut}/splitCard_${region}.txt`
	echo ${command}	

	command=`sed -i '/scale/ a pdfindex_'${region}'_13TeV discrete' ${dirOut}/splitCard_${region}.txt`
	echo ${command}	

    fi
done


