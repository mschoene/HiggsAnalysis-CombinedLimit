#!/bin/bash                                                                                                                                                                          
echo $#;
if [ $# != 4 ]; then
    echo "USAGE: ${0} MODEL PATH M1 M2";
    exit;
fi

MODEL=$1
MYPATH=$2
M1=$3
M2=$4

#MYCARD="${MYPATH}/datacard_${MODEL}_${M1}_${M2}_combined.txt

#MYCARD="${MYPATH}/datacard_${MODEL}_${M1}_${M2}_combined.txt
if [[ $MODEL == "T2bH" ]]
then
    M1="mSbottom"$M1
    M2="mLSP"$M2
    MYCARD="${MYPATH}/Datacard_13TeV_SMS_${MODEL}_${M1}_${M2}.txt"
fi


if [[ $MODEL == "TChiWH" ]]
then
    M1="HToGG_m"$M1
    MYCARD="${MYPATH}/Datacard_13TeV_SMS_${MODEL}_${M1}_m${M2}.txt"
fi



if [[ $MODEL == "TChiHH" ]]
then
    M1="HToGG_m"$M1
    MYCARD="${MYPATH}/Datacard_13TeV_SMS_${MODEL}_${M1}.txt"
fi

if [[ $MODEL == "TChiHZ" ]]
then
    M1="HToGG_m"$M1
    MYCARD="${MYPATH}/Datacard_13TeV_SMS_${MODEL}_${M1}.txt"
fi





echo MYCARD

source $VO_CMS_SW_DIR/cmsset_default.sh
# #source /mnt/t3nfs01/data01/swshare/glite/external/etc/profile.d/grid-env.sh
export SCRAM_ARCH=slc6_amd64_gcc491
export LD_LIBRARY_PATH=/mnt/t3nfs01/data01/swshare/glite/d-cache/dcap/lib/:$LD_LIBRARY_PATH

echo "Loading CMSSW_7_4_7"
cd /work/mschoene/CMSSW_7_4_7_gg/src/HiggsAnalysis/CombinedLimit
echo $PWD
eval `scramv1 runtime -sh`

JOBDIR=/scratch/`whoami`/significanceCalculation_${JOB_ID}/

mkdir -p ${JOBDIR}

echo $MYCARD

cd ${JOBDIR}

echo "card ${MYCARD}"
#command=`dccp dcap://t3se01.psi.ch:22125/${MYCARD} ${JOBDIR}/`
command=`cp ${MYCARD} ${JOBDIR}/`
echo ${command}

#command=`cp /work/mschoene/CMSSW_7_4_7_gg/src/HiggsAnalysis/CombinedLimit/CMS-HGG_multipdf_data_dec01_noLau.root ${JOBDIR}/`
command=`cp /work/mschoene/CMSSW_7_4_7_gg/src/HiggsAnalysis/CombinedLimit/CMS-HGG_multipdf_data_mar20.root ${JOBDIR}/`
echo ${command}


if [[ $MODEL == "TChiWH" ]]
then
    MODEL="WH"
fi

if [[ $MODEL == "TChiHH" ]]
then
    MODEL="HH"
fi

if [[ $MODEL == "TChiHZ" ]]
then
    MODEL="HZ"
fi

command=`cp /work/mschoene/CMSSW_7_4_7_gg/src/HiggsAnalysis/CombinedLimit/CMS-HGG_13TeV_sigfit_2019mar20_${MODEL}*.root ${JOBDIR}/`
echo ${command}

command=`cp /work/mschoene/CMSSW_7_4_7_gg/src/HiggsAnalysis/CombinedLimit/CMS-HGG_13TeV_sigfit_2019mar20_Higgs.root ${JOBDIR}/`
echo ${command}



#command=`combine -M Asymptotic datacard_${MODEL}_${M1}_${M2}_combined.txt -n ${MODEL}_${M1}_${M2} >& log_${MODEL}_${M1}_${M2}_combined.txt`
command=`combine -M ProfileLikelihood --significance --rMin -5 --uncapped 1  -m 125 $MYCARD  >& ${MYCARD}.siglog`

#command=`combine -M ProfileLikelihood --significance datacard_all_${MODEL}_${M1}_${M2}.txt -n ${MODEL}_${M1}_${M2} --rMin -5 --uncapped 1 >& log_${MODEL}_${M1}_${M2}_combined.txt`

echo $command

command=`cp  ${MYCARD}.siglog ${MYPATH}/significance/`
echo $command

# xrdcp -v log_${MODEL}_${M1}_${M2}_combined.txt root://t3dcachedb.psi.ch:1094//${MYPATH}/limits/log_${MODEL}_${M1}_${M2}_combined.txt

rm -rf $JOBDIR
