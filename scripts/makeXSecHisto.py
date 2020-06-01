import ROOT, array
from ROOT import TF1, TH1, TGraph
import sys, glob, math
ROOT.gROOT.SetBatch(True)
lumi = 78.3
#lumi = 35.9
branching_ratio = 1.0 # already accounted for in datacards
#branching_ratio = 0.25

fxsec = None
hxsec = None

if len(sys.argv)!=2:
    print "python (-i) make1DLimit_LQ.py <model>, with <model>=T2tt,T2qq,T2bb"
    exit()

model = sys.argv[1]


  
def main():
    version = "limits_0"
    dir="./"+version+"/"


    if model=="WH" or model=="HH" or model=="HZ":
        if model=="WH":
            f_xsecgraph = ROOT.TFile.Open("/shome/mschoene/8_0_12_newRmDup/src/myMT2Analysis/Utils/C1N2_wino_13TeV.root")
            name = "C1N1_wino"
        else:
            f_xsecgraph = ROOT.TFile.Open("/shome/mschoene/8_0_12_newRmDup/src/myMT2Analysis/Utils/CN_hino_13TeV.root")
            name = "CN_hino"

        param =  f_xsecgraph.Get("nFits");
        nFits = param.GetVal();

    #Find the cross-section
        
        fitName="";
        fitTitle="";
        tokens=[];
    
        crossSectionNom = 0.
        crossSectionUp = 0.
        crossSectionDn = 0.
        crossSectionUnc = 0.

        g_xsec_slq=ROOT.TGraph()
        g_xsec_slqU=ROOT.TGraph()
        g_xsec_slqD=ROOT.TGraph()

        xs=ROOT.TH1F("xs",'', 1001, 0, 1000) 
# "h_xsec:slq", mass[ len(mass)-1] , mass[ 0],mass[ len(mass)-1] )

        # for m in range( 125, 139 ):       
        for m in range(100, 1000 ):       #
            for i in range(0,nFits):
                #        Read the functions
                fitName="fit_nom_"+ str(i)
                funcNom = f_xsecgraph.Get(fitName);
                fitName="fit_up_"+ str(i)
                funcUp = f_xsecgraph.Get(fitName);
                fitName="fit_dn_"+ str(i)        
                funcDn = f_xsecgraph.Get(fitName);

            # Find the title that holds the min_max values
                fitTitle =  funcNom.GetTitle();
                tokens   = fitTitle.split("_");
                lowPoint = tokens[2]
                highPoint = tokens[3]
            

            # Check to see if the mass matches
                if(m >= int(lowPoint)  and m < int(highPoint) ):
                    crossSectionNom = funcNom.Eval(m);
                    crossSectionUp  = funcUp.Eval(m);
                    crossSectionDn  = funcDn.Eval(m);
                    if(crossSectionUp-crossSectionNom > crossSectionNom-crossSectionDn):
                        crossSectionUnc = crossSectionUp-crossSectionNom
                    else:
                        crossSectionUnc = crossSectionNom-crossSectionDn;

                #print m, crossSectionNom
                #               g_xsec_slq.SetPoint(m, m, crossSectionNom/1000.)
                #               g_xsec_slqU.SetPoint(m, m, (crossSectionNom + crossSectionUnc)/1000.)
                #               g_xsec_slqD.SetPoint(m, m, (crossSectionNom - crossSectionUnc)/1000.)
                #                xs.Fill( m , crossSectionNom/1000.)

                xs.SetBinContent( xs.FindBin(m) , crossSectionNom/1000.)
                xs.SetBinError( xs.FindBin(m) , crossSectionUnc/1000.)
            
                break;



    else:
        
        if model=="bb" :
            xsFile = "/shome/mschoene/SUSxsecs/SUSYCrossSections13TeVstopstop_2019Feb08.txt"
            name = "stopstop_2019Feb08"

        else:
            xsFile = "/shome/mschoene/SUSxsecs/SUSYCrossSections13TeVgluglu_2019Feb08.txt"
            name = "gluglu_2019Feb08"

        fitName="";
        fitTitle="";
        tokens=[];
    
        crossSectionNom = 0.
        crossSectionUp = 0.
        crossSectionDn = 0.
        crossSectionUnc = 0.

        if model=="bb" :
            xs=ROOT.TH1F("xs",'', 581, 97.5, 3002.5) 
        else:
            xs=ROOT.TH1F("xs",'', 501, 497.5, 3002.5) 
            
        with open(xsFile) as i:
            lines = i.readlines()
            for line in lines:
                if ("#" in line ) : continue
                line.replace("  "," ")
                words=line.split(" ")
                #                if not ("125.0" in words[0]) : continue
#                print "proc " , proc , " found ", words[0], " xs ", words[1]
#                print words[0],float(words[3])
                xs.FindBin( float(words[0]) )
                xs.SetBinContent( xs.FindBin( float(words[0])) , float(words[3]) )
                xs.SetBinError( xs.FindBin( float(words[0])) , float(words[5])/100.*float(words[3]) )
#                

    f_out = ROOT.TFile("SUSYCrossSections13TeV"+name+".root","RECREATE")
    f_out.cd()

    xs.Write()
    
    f_out.Close()


#####################################################################################################
if __name__ == "__main__":
    main()
