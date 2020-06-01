#!/usr/bin/env python
from math import *
import os, commands
from sys import argv,exit
from optparse import OptionParser
import ROOT

print "running:", argv

if len(argv)<2:
    print "Usage: "+argv[0]+" fileWithSignificance.txt"
    exit(1)

INPUT = argv[1]

# get contours separately for the left and right side of the deltaM=Mtop diagonal (T2tt)
divideTopDiagonal = False


models   = ["T1bbbb","T1tttt","T1qqqq","T2qq","T2bb","T2tt","T2cc","T2bH","WH"]
model = "mymodel"
for m in models:
    if m in INPUT:
        model = m

print "model =", model

pvalues = ["pvalue"]

# coloum-limit map for txt files (n -> column n+1) 
fileMap = {"pvalue":3}


def getSigYN ( h_pvalue, r_excluded=0.5):
    name = h_pvalue.GetName().replace("pvalue","yn")
    h_sig_yn = h_pvalue.Clone(name)
    for ix in range(1,h_sig_yn.GetNbinsX()+1):
        for iy in range(1,h_sig_yn.GetNbinsY()+1):
            r = h_sig_yn.GetBinContent(ix,iy)
            h_sig_yn.SetBinContent(ix, iy, 1e-3 if r<r_excluded else 1 if r>0 else 0)
    return h_sig_yn
    
def getSig ( h_pvalue ):
    name = h_pvalue.GetName().replace("pvalue","sig")
    h_sig = h_pvalue.Clone(name)
    for ix in range(1,h_sig.GetNbinsX()+1):
        m = h_sig.GetXaxis().GetBinCenter(ix)
        for iy in range(1,h_sig.GetNbinsY()+1):
            r = h_sig.GetBinContent(ix,iy)
            if r==0:
                sig=-99.
            else:
                sig  = ROOT.TMath.NormQuantile(1-r)
            h_sig.SetBinContent(ix, iy, sig)
    return h_sig
    

def readPvaluesFromFile(INPUT, fileMap, h_pvalue0, h_sig0, h_sig_yn0):
    rlim = {}
    for line in open(INPUT, "r"):
        m1        = float(line.split()[0])
        m2        = float(line.split()[1])
        for lim,index in fileMap.iteritems():
            rlim[lim]  = float(line.split()[index])

        rlim['sig'] = ROOT.TMath.NormQuantile(1-(rlim['pvalue']))

        #fill the 2d limit histos
        binX=h_pvalue0[lim].GetXaxis().FindBin(m1)
        binY=h_pvalue0[lim].GetYaxis().FindBin(m2)
    
        for lim in pvalues:
            h_pvalue0[lim].SetBinContent(binX, binY, rlim[lim])
            h_sig0[lim].SetBinContent(binX, binY, ROOT.TMath.NormQuantile(1-(rlim[lim])))
            h_sig_yn0[lim].SetBinContent(binX, binY, 1 if rlim[lim]>0.5 else 1e-3)


def interpolateDiagonal(hist):
    # interpolate in diagonal direction to fill remaining missing holes
    # start from 15 bins away and finish in the diagonal
    Nx = hist.GetNbinsX() 
    Ny = hist.GetNbinsY()
    for i in range(14,-1,-1): # 14...0
        j=0
        while i+j<Nx and j<Ny:
           j+=1
           val1=hist.GetBinContent(i+j,j)
           if val1==0 or hist.GetBinContent(i+j+1,j+1)!=0:
               continue

           n=2
           while hist.GetBinContent(i+j+n,j+n)==0 and i+j+n<Nx and j+n<Ny:
               n+=1
           val2 = hist.GetBinContent(i+j+n,j+n)
           if val2==0:
               continue
           for nn in range(1,n):                    
               hist.SetBinContent(i+j+nn,j+nn,val1+(val2-val1)*nn/n) 


def unexcludeDiagonal(hist, mSplit=175): 
    for ix in range(1,hist.GetNbinsX()+1):
        for iy in range(1,hist.GetNbinsY()+1):
            m1, m2 = hist.GetXaxis().GetBinLowEdge(ix), hist.GetYaxis().GetBinLowEdge(iy)
            val = hist.GetBinContent(ix,iy)
            if m1-m2==mSplit:
                hist.SetBinContent(ix,iy, max(1.5,val))

h_pvalue0 = {} # pvalue, original binning
h_sig_yn0 = {} # pvalue in excess/deficit, original binning
h_sig0    = {} # significance, original binning

h_pvalue   = {} # pvalue, interpolated
h_sig_yn   = {} # pvalue in excess/deficit, interpolated
h_sig      = {} # significance, interpolated
g2_pvalue  = {} # TGraph2D pvalue, automatic interpolation

m1min, m1max = 0, 2300
m2min, m2max = 0, 2300
xbinSize = 5
#xbinSize = 25 if model!='T2cc' else 5
ybinSize = 5 if model!='T2cc' else 5

mass1 = "m_{#tilde{g}}" if "T1" in model else "m_{#tilde{q}}" if model=="T2qq" else "m_{#tilde{b}}" if model=="T2bb" else "m_{#tilde{t}}" if model=="T2tt" else "mChi2" if model=="WH" else "m1"

mass2 = "m_{#tilde{#chi_{1}^{0}}}"

# create histos
for lim in pvalues:
    # uniform 25 GeV binning
    h_pvalue0[lim] = ROOT.TH2F(lim+"_pvalue0", model, (m1max-m1min+xbinSize)/xbinSize, m1min-xbinSize/2., m1max+xbinSize/2., (m2max-m2min+2*ybinSize)/(ybinSize), m2min-3*ybinSize/2., m2max+ybinSize/2.)
    h_pvalue0[lim].SetXTitle(mass1)    
    h_pvalue0[lim].SetYTitle(mass2)    
                                       
    h_sig_yn0[lim] = h_pvalue0[lim].Clone(h_pvalue0[lim].GetName().replace("pvalue","sig_yn"))
    h_sig0[lim]    = h_pvalue0[lim].Clone(h_pvalue0[lim].GetName().replace("pvalue","sig"))


# read txt file with limits (map defined above)
print "reading file..."
readPvaluesFromFile(INPUT, fileMap, h_pvalue0, h_sig0, h_sig_yn0)

# so graph goes below mLSP=0 and there is no cut off above zero
def fillHorizontalBelowZero(hist):
    for ix in range(1,hist.GetNbinsX()+1):
        hist.SetBinContent( ix,1,hist.GetBinContent(ix,2) )

output = INPUT.replace(".txt", ".root")
fout = ROOT.TFile(output, "RECREATE")
fout.cd()

print "interpolating..."
for lim in pvalues:
    fillHorizontalBelowZero(h_pvalue0[lim])
    # interpolation done automatically by TGraph2D using Delaunay method
    g2_pvalue[lim] = ROOT.TGraph2D(h_pvalue0[lim])
    xbinSize_inter = xbinSize/2.
    #xbinSize_inter = xbinSize/2. if model!='T2cc' else ybinSize # bin size of interpolation graph (12.5 GeV as decided in dec7 meeting @ R40) 
    ybinSize_inter = ybinSize/2. if model!='T2cc' else ybinSize # bin size of interpolation graph (12.5 GeV as decided in dec7 meeting @ R40) 
    g2_pvalue[lim].SetNpx( int((g2_pvalue[lim].GetXmax()-g2_pvalue[lim].GetXmin())/xbinSize_inter) )
    g2_pvalue[lim].SetNpy( int((g2_pvalue[lim].GetYmax()-g2_pvalue[lim].GetYmin())/ybinSize_inter) )
    h_pvalue[lim] = g2_pvalue[lim].GetHistogram()
    h_pvalue[lim].SetName( h_pvalue0[lim].GetName().replace("pvalue0","pvalue") )
             
    #remove negative or nan bins that appear in T2qq for no apparent reason
    for ix in range(1,h_pvalue[lim].GetNbinsX()+1):
        for iy in range(1,h_pvalue[lim].GetNbinsY()+1):
            if h_pvalue[lim].GetBinContent(ix,iy) < 0: #if negative set to zero
                h_pvalue[lim].SetBinContent(ix,iy,0)
            if isnan(h_pvalue[lim].GetBinContent(ix,iy)): #if nan set to neighbour average
                val = (h_pvalue[lim].GetBinContent(ix+1,iy) + h_pvalue[lim].GetBinContent(ix-1,iy) + h_pvalue[lim].GetBinContent(ix,iy+1) + h_pvalue[lim].GetBinContent(ix,iy-1) )/4.0
                h_pvalue[lim].SetBinContent(ix,iy,val)



print "translating to significance and yes/no limits and saving 2d histos..."
for lim in pvalues:
    #if model=="T2tt":
    #    unexcludeDiagonal( h_pvalue[lim])
    #if model=="T2bb":  # do this for summary plot as per FKW request
    #    unexcludeDiagonal( h_pvalue[lim],25 )    
    #    unexcludeDiagonal( h_pvalue[lim],37.5 )    
    
    h_sig_yn[lim] = getSigYN ( h_pvalue[lim] )
    h_sig[lim] = getSig ( h_pvalue[lim] )
    
    h_pvalue0[lim].Write()
    h_sig0[lim].Write()
    h_sig_yn0[lim].Write()
    h_pvalue [lim].Write()
    h_sig [lim].Write()
    h_sig_yn [lim].Write()



print "saving x-check plots"
plotsDir = "xcheckPlotsSignificance"
can = ROOT.TCanvas("can","can",600,600)
if( not os.path.isdir(plotsDir) ):
    os.system("mkdir "+plotsDir)
for lim in pvalues:
    ROOT.gStyle.SetNumberContours( 100 )
    xmin = 600 if "T1" in model else 150 if model=="T2tt" or model=='T2cc' else 300 if model=="T2bb" else 200 if model=="T2bH"  else 350 if model=="T2qq" else  100 if model=="WH" else 0
    xmax = 1200 if model=="T2tt"  or model=="T2bb" else  400 if model=="WH" else 1600 if model=="T2qq" else 1100 if model=="T2bH" else 800 if model=='T2cc' else 2300 if model=="T1bbbb" else 2300
    ymax = 700  if model=="T2tt" else 800 if model=="T2bb" else  400 if model=="WH" else 1000 if model=="T2bH" or model=="T2cc" else 1200 if model=="T2qq" else 1800


#    xmin = 600 if "T1" in model else 150 if model=="T2tt" or model=='T2cc' else 300 if model=="T2bb" else 300 if model=="T2qq" else 0
#    xmax = 1400 if model=="T2tt"  or model=="T2bb" else 1800 if model=="T2qq" else 900 if model=='T2cc' else 2300 if model=="T1bbbb" else 2300
#    ymax = 700  if model=="T2tt" else 800 if model=="T2bb" or model=="T2cc" else 1200 if model=="T2qq" else 1800

    h_sig0[lim].GetXaxis().SetRangeUser(xmin, xmax)
    h_sig0[lim].GetYaxis().SetRangeUser(0   , ymax)
    h_sig0[lim].Draw("colz")
    can.SaveAs(plotsDir+"/" + model + "_sig0.eps")
    can.SaveAs(plotsDir+"/" + model + "_sig0.png")
    can.SaveAs(plotsDir+"/" + model + "_sig0.pdf")


print "file "+output+" saved"
#fout.Close()
