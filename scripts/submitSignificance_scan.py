import os
import sys
import commands

from os import listdir
from os.path import isfile, join
import os,sys,copy,math,re

if len(sys.argv)>1:
    folderName = sys.argv[1]
else:
    folderName = "dataCards_HZ_dec01"

mypath ="/shome/mschoene/CMSSW_7_4_7_gg/src/HiggsAnalysis/CombinedLimit/" 

#shome/mschoene/CMSSW_7_4_7_gg/src/HiggsAnalysis/CombinedLimit

#"/pnfs/psi.ch/cms/trivcat/store/user/casal/EventYields_data_Run2016_7p7ifb/datacards_T2bb_final/"

#models   = ["T1bbbb", "T1tttt","T1qqqq","T2qq","T2bb","T2tt"]
#for m in models:
#    if m in mypath:
#        model = m

#command = "gfal-mkdir -p srm://t3se01.psi.ch/"+mypath+"limits/"
command = "mkdir "+mypath+folderName+"/significance/"
os.system(command)


for f in listdir(mypath+folderName):

    if ".txt" not in f:
        continue

    if "Datacard" not in f:
        continue

    if ".log" in f:
        continue

    print " "
    print f
    model=f.split("_")[3]

    regex = re.compile('Sbottom([0-9]*)')
    regex2 = re.compile('mLSP([0-9]*)')
    mSbottom = regex.findall( f )
    mChi = regex2.findall( f )

    
    if( "TChiH" in f):
        regex = re.compile('HToGG_m([0-9]*)')
        regex2 = re.compile('_([0-9]*).')
        
    if( "TChiWH" in f):
        regex = re.compile('HToGG_m([0-9]*)')
        regex2 = re.compile('_m([0-9]*)')
            
    mSbottom = regex.findall( f )
    mChi = regex2.findall( f )

    m1 = list(map(float, mSbottom))
    m2=list([1])



    if( not "TChiH" in f and not "TChiWH" in f):
        m2=int(mChi[0])
    elif(  "TChiWH" in f):
        m2 = int(mChi[1])


    m1=int(m1[0])
    print model, m1, m2
    print str(m1)

    # # check if file exists and is non-empty
    logfile = mypath+folderName+"/significance/log_"+model+"_"+str(m1)+"_"+str(m2)+".txt"
    if ( os.path.isfile(logfile) ):
        print "file exists... skiping:",logfile
        continue

    command="qsub -q all.q -o /dev/null -e /dev/null -N sig_"+model+"_"+str(m1)+"_"+str(m2)+" scripts/submitSignificance_batch_scan.sh "+model+" "+mypath+folderName+" "+str(m1)+" "+str(m2)
    print command
    os.system(command)

