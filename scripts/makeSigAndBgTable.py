
import os,sys,copy,math,re
###############################################################################

###############################################################################
## PARSE ROOT MACROS  #########################################################
###############################################################################
import ROOT as r
#if options.quadInterpolate:
#  r.gROOT.ProcessLine(".L quadInterpolate.C+g")
#  from ROOT import quadInterpolate
r.gROOT.ProcessLine(".L $CMSSW_BASE/lib/$SCRAM_ARCH/libHiggsAnalysisCombinedLimit.so")
#r.gROOT.ProcessLine(".L ../libLoopAll.so")
###############################################################################

###############################################################################
## WSTFileWrapper  ############################################################
###############################################################################

class WSTFileWrapper:
   #self.fnList = [] # filename list
   #self.fileList = [] #file list
   #self.wsList = [] #workspace list

   def __init__(self, files,wsname):
      self.fnList = files.split(",") # [1]       
      self.fileList = []
      self.wsList = [] #now list of ws names...
    #print files
      for fn in self.fnList: # [2]
         f = r.TFile.Open(fn) 
         self.fileList.append(f)
         thing = f.Get(wsname)
         self.wsList.append(self.fileList[-1].Get(wsname))
         f.Close()

   def data(self,dataName):
      result = None
      complained_yet =0 
      for i in range(len(self.fnList)):
         this_result_obj = self.wsList[i].data(dataName);
         if ( result and this_result_obj and (not complained_yet) ):
            complained_yet = true;
         if this_result_obj: # [3]
            result = this_result_obj
            return result 

   def pdf(self,dataName):
      result = None
      complained_yet =0 
      for i in range(len(self.fnList)):
         this_result_obj = self.wsList[i].pdf(dataName);
         if ( result and this_result_obj and (not complained_yet) ):
            complained_yet = true;
         if this_result_obj: # [3]
            result = this_result_obj
            return result 
      
   def var(self,varName):
      result = None
      complained_yet =0 
      for i in range(len(self.fnList)):
         this_result_obj = self.wsList[i].var(varName);
         if this_result_obj: # [3]
            result = this_result_obj
            
            return result 


###############################################################################
###############################################################################
###############################################################################

# directory to cross section
xsecFileName="/shome/casal/SUSxsecs/SUSYCrossSections13TeV"
# path to full table
fulltable = open("/mnt/t3nfs01/data01/shome/casal/CMSSW_7_4_12_patch4_MT2/src/analysisJul/analysis/latexBGTable_EventYields_data_Run2016_7p7ifb.tex", "r")

inputFileName="CMS-HGG_13TeV_sigfit_oct27_T2bH_b012ISR.root"

inputFile = r.TFile ( inputFileName )
inWS = WSTFileWrapper( inputFileName,"wsig_13TeV")
#inWS = inputFile.Get('wsig_13TeV')

proc = "SMS_T2bH_mSbottom250_mLSP100"
cat = "HT0toInf_j0_b0toInf_pT0"

mass = inWS.var("hgg_mass")
#weight = r.RooRealVar("weight","weight",0)
data_nominal= inWS.data("sig_%s_mass_m%d_%s"%(proc,125,cat))
#data_nominal= inWS.data("%s_%d_13TeV_%s_pdfWeights"%(proc,125,cat))

#data_nominal_sum = data_nominal.sumEntries()

#if (data_nominal_sum <= 0.):
#    print "[WARNING] This dataset has 0 or negative sum of weight. Systematic calulcxation meaningless, so list as '- '"

#print "sig_%s_mass_m%d_%s"%(proc,125,cat)
print "dataSet = ", data_nominal

pdf = inWS.pdf("hggpdfsmrel_13TeV_%s_%s"%(proc,cat))

print "pdf = ", pdf.Print()
mass.setVal(125)
mass.setRange("FWHM",120,130)
print "pdf = ", pdf.evaluate()
print "pdf = ", pdf.createIntegral(mass, NormSet(mass), Range("cut") )





#print inWS.Print()
#print inWS.find(hggpdfsmrel_13TeV_SMS_T2bH_mSbottom450_mLSP1_HT0toInf_j0_b0toInf_pT0).evaluate()



# if len(sys.argv)<3:
#     print "Usage: "+sys.argv[0]+" model lumi(fb) [limits.txt]"
#     exit(1)

# modelpoint = str  (sys.argv[1])
# model = modelpoint.split("_")[0]
# m1    = modelpoint.split("_")[1]
# m2    = modelpoint.split("_")[2]

# lumi  = float(sys.argv[2])

# exp = "xxx"
# if len(sys.argv) >3:
#     limits = open(sys.argv[3] , "r").readlines()
#     for l in limits:
#         if l.split()[0]==m1 and l.split()[1]==m2:
#             exp = l.split()[2]
           


#dataCards_T2bH_oct27_b012ISR/AsymptoticRanking_SMS_T2bH_mSbottom_450_1.txt

# shapes SMS_T2bH_mSbottom450_mLSP1 
# HT0toInf_j0_b0toInf_pT0 
# CMS-HGG_13TeV_sigfit_oct27_T2bH_b012ISR.root

# wsig_13TeV:hggpdfsmrel_13TeV_SMS_T2bH_mSbottom450_mLSP1_HT0toInf_j0_b0toInf_pT0

# hws::hgg_mass.setVal(125)
# hws::hggpdfsmrel_13TeV_SMS_T2bH_mSbottom450_mLSP1_HT0toInf_j0_b0toInf_pT0.evaluate()





# iter = fit_s.createIterator()
# Headline = "%-30s %-30s     pre-fit   signal+background Fit  bkg-only Fit"%("Channel","Process") if (prefit and errors) else "%-30s %-30s  signal+background Fit  bkg-only Fit"%("Channel","Process")
# print Headline

# while True:
#     norm_s = iter.Next()
#     if norm_s == None: break;

#     norm_b = fit_b.find(norm_s.GetName())

#     print "%-30s %-30s %7.3f %7.3f" % (m.group(1), m.group(2), norm_s.getVal(), norm_b.getVal())
