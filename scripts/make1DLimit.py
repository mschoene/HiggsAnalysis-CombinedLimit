import ROOT, array
from ROOT import TF1, TH1, TGraph, TLegend, TLatex, TH2
import sys, glob, math
ROOT.gROOT.SetBatch(True)
lumi = 77.5
#lumi = 78.3
#lumi = 35.9
branching_ratio = 1.0 # already accounted for in datacards
#branching_ratio = 0.25

fxsec = None
hxsec = None

if len(sys.argv)!=2:
    print "python (-i) make1DLimit_LQ.py <model>, with <model>=T2tt,T2qq,T2bb"
    exit()

model = sys.argv[1]

mass=[]
obs=[]
exp=[]
em2s=[]
em1s=[]
ep1s=[]
ep2s=[]

def get1Dlimit(fn,t2):
    global mass
    global exp
    global obs
    global ep1s
    global em1s
    global ep2s
    global em2s
    f = open(fn, "r")
    for l in f.readlines():
        if int(l.split()[0])> 500:
            continue
#        if(int(l.split()[1])!=0):
#            print l.split()[1]
#            continue
        if(t2=="T2tt" and int(l.split()[0])<300):
            continue
#        if(t2=="T2bb" and (int(l.split()[0])>1500 and int(l.split()[0])<1650)):
#            continue
        mass.append(int(l.split()[0]))
        exp.append(float(l.split()[1]))
        obs.append(float(l.split()[2]))
        ep1s.append(float(l.split()[3]))
        em1s.append(float(l.split()[4]))
        ep2s.append(float(l.split()[5]))
        em2s.append(float(l.split()[6]))

#        ep1s.append(float(l.split()[3]))
#        em1s.append(float(l.split()[4]))
#        ep2s.append(float(l.split()[5]))
#        em2s.append(float(l.split()[6]))

        

def get1Dxsec(smass):
    global fxsec, hxsec
    if not fxsec or not hxsec:
        fxsec = ROOT.TFile.Open("../babymaker/data/xsec_susy_13tev.root")
        if model!="T2qq":
            hxsec = fxsec.Get("h_xsec_stop")
        else:
            hxsec = fxsec.Get("h_xsec_squark")

    sigma = hxsec.GetBinContent(hxsec.FindBin(smass)) 
 

#    sigma = hxsec.GetBinContent(hxsec.FindBin(smass)) 
    return sigma
  
xnorm=1.0
#if model=="T2qq":
#    xnorm =8.0
  
def main():
    version = "limits_0"
    dir="./"+version+"/"



    if model=="T2tt":
        fn = '../babymaker/data/limits_T2tt_full_Moriond2017.txt'
    elif model=="HH":
        fn = 'dataCards_HH_mar30/limits/limits_SMS_TChiHH_HToGG.txt'
    elif model=="HZ":
        fn = 'dataCards_HZ_mar30_corrSumGenMET/limits/limits_SMS_TChiHZ_HToGG.txt'
    else:
        print "Are you sure you know what you're doing?"
        exit()

    # if model=="T2tt":
    #     fn = '../babymaker/data/limits_T2tt_full_Moriond2017.txt'
    # elif model=="HH":
    #     fn = 'dataCards_HH_aug16/limits_SMS_TChiHH_HToGG.txt'
    # elif model=="HZ":
    #     fn = 'dataCards_HZ_aug16/limits_SMS_TChiHZ_HToGG.txt'
    # else:
    #     print "Are you sure you know what you're doing?"
    #     exit()

    get1Dlimit(fn, model)

    if model=="WH":
        f_xsecgraph = ROOT.TFile.Open("/shome/mschoene/8_0_12_newRmDup/src/myMT2Analysis/Utils/C1N2_wino_13TeV.root")
    else:
        f_xsecgraph = ROOT.TFile.Open("/shome/mschoene/8_0_12_newRmDup/src/myMT2Analysis/Utils/CN_hino_13TeV.root")


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

    h_xsec_slq=ROOT.TH1F("name",'', 1001, 0, 1000) 
 # "h_xsec:slq", mass[ len(mass)-1] , mass[ 0],mass[ len(mass)-1] )


   # for m in range( 125, 139 ):       
    for m in range(100, mass[ len(mass)-1]  ):       #
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
 
            # c12 = ROOT.TCanvas("c12", "", 800, 800)
            # c12.cd()
            # testpad = ROOT.TPad("p_tex", "p_tex", 0.0, 0.0, 1.0, 1.0)
            # testpad.SetTopMargin(0.1)
            # testpad.SetBottomMargin(0.1)
            # testpad.SetRightMargin(0.05)
            # testpad.SetLeftMargin(0.15)
            # testpad.Draw()
            # funcNom.Draw()

            # c12.SaveAs("test.png")
    

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
                g_xsec_slq.SetPoint(m, m, crossSectionNom/1000.)
                g_xsec_slqU.SetPoint(m, m, (crossSectionNom + crossSectionUnc)/1000.)
                g_xsec_slqD.SetPoint(m, m, (crossSectionNom - crossSectionUnc)/1000.)
                h_xsec_slq.Fill( m , crossSectionNom/1000.)
            
                break;
        

    # g_xsec_slq = f_xsecgraph.Get("slqxsec")

    # f_xsecgraph = ROOT.TFile.Open("../babymaker/data/lq-xsec-MG-NNPDF-graph_0p25_k.root")
    # g_xsec_slq = f_xsecgraph.Get("slqxsec")
    # g_xsec_vlq = f_xsecgraph.Get("vlqxsec")
    # g_xsec_slqU = f_xsecgraph.Get("slqxsecUp")
    # g_xsec_vlqU = f_xsecgraph.Get("vlqxsecUp")
    # g_xsec_slqD = f_xsecgraph.Get("slqxsecDown")
    # g_xsec_vlqD = f_xsecgraph.Get("vlqxsecDown")
    # g_xsec0p25_vlq  = f_xsecgraph.Get("vlqxsec0p25")
    # g_xsec0p25_slqU = f_xsecgraph.Get("slqxsec0p25Up")
    # g_xsec0p25_vlqU = f_xsecgraph.Get("vlqxsec0p25Up")
    # g_xsec0p25_slqD = f_xsecgraph.Get("slqxsec0p25Down")
    # g_xsec0p25_vlqD = f_xsecgraph.Get("vlqxsec0p25Down")

    # g_xseck0_vlq  = f_xsecgraph.Get("vlqxsec_k0")
    # g_xseck0_vlqU = f_xsecgraph.Get("vlqxsecUp_k0")
    # g_xseck0_vlqD = f_xsecgraph.Get("vlqxsecDown_k0")

    # g_xseck0_0p25_vlq  = f_xsecgraph.Get("vlqxsec0p25_k0")
    # g_xseck0_0p25_vlqU = f_xsecgraph.Get("vlqxsec0p25Up_k0")
    # g_xseck0_0p25_vlqD = f_xsecgraph.Get("vlqxsec0p25Down_k0")



###    f_xsecgraphS = ROOT.TFile.Open("../babymaker/data/lq-xsec-graph.root")
###    g_xsec_slq = f_xsecgraphS.Get("slqxsec")
###    g_xsec_slqU = f_xsecgraphS.Get("slqxsec")
###    g_xsec_slqD = f_xsecgraphS.Get("slqxsec")




    sigmas = []
    
    x0e=[]
    m2s=[]
    m1s=[]
    p1s=[]
    p2s=[]

    xmin = float(mass[0])-12.5
    xmax = float(mass[len(mass)-1])+12.5
    nbins = int((xmax-xmin)/25)
    
    for i in range(0,len(mass)):
        tmpX, tmpY = ROOT.Double(0), ROOT.Double(0)
        g_xsec_slq.GetPoint(mass[i], tmpX, tmpY)
        xsec = h_xsec_slq.GetBinContent(h_xsec_slq.FindBin( mass[i] ))
        sigmas.append(xsec) 
        sigmas[i] = sigmas[i]*xnorm
        exp[i] = exp[i]*sigmas[i]
        obs[i] = obs[i]*sigmas[i]
        em1s[i] = em1s[i]*sigmas[i]
        ep1s[i] = ep1s[i]*sigmas[i]
        em2s[i] = em2s[i]*sigmas[i]
        ep2s[i] = ep2s[i]*sigmas[i]

    for i in range(0,len(mass)):
        m2s.append(exp[i]-em2s[i])
        m1s.append(exp[i]-em1s[i])
        p1s.append(ep1s[i]-exp[i])
        p2s.append(ep2s[i]-exp[i])
        x0e.append(0.)
    

 
    ppSqSq = "pp #rightarrow #chi#chi"

    branching = ""



    if model=="HH":
        ppSqSq = "pp #rightarrow #tilde{#chi}^{0,#pm}_{i} #tilde{#chi}^{0,#pm}_{j} #rightarrow  #tilde{#chi}^{0}_{1} #tilde{#chi}^{0}_{1} + X_{soft}; #tilde{#chi}^{0}_{1} #rightarrow H #tilde{G} (100%)"
        branching="m_{#tilde{G}} = 1 GeV;  m_{#tilde{#chi}^{0}_{2}} #approx m_{#tilde{#chi}^{#pm}_{1}} #approx m_{#tilde{#chi}^{0}_{1}}"
    elif model=="HZ":
        ppSqSq =  "pp #rightarrow #tilde{#chi}^{0,#pm}_{i} #tilde{#chi}^{0,#pm}_{j} #rightarrow  #tilde{#chi}^{0}_{1} #tilde{#chi}^{0}_{1} + X_{soft}; #tilde{#chi}^{0}_{1} #rightarrow H #tilde{G} (50%)"
        branching="#tilde{#chi}^{0}_{1} #rightarrow Z #tilde{G} (50%)"
        lightSq="m_{#tilde{G}} = 1 GeV;  m_{#tilde{#chi}^{0}_{2}} #approx m_{#tilde{#chi}^{#pm}_{1}} #approx m_{#tilde{#chi}^{0}_{1}}"


    # if model=="HH":
    #     ppSqSq = "pp #rightarrow #tilde{#chi}_{1}^{#pm,0} #tilde{#chi}_{1}^{#pm,0} #rightarrow #tilde{#chi}_{1}^{0} #tilde{#chi}_{1}^{0} + X_{soft} "
    #     branching=" #tilde{#chi}_{1}^{0} #rightarrow H #tilde{G} (100%) ";
    # elif model=="HZ":
    #     ppSqSq = "pp #rightarrow #tilde{#chi}_{1}^{#pm,0} #tilde{#chi}_{1}^{#pm,0} #rightarrow #tilde{#chi}_{1}^{0} #tilde{#chi}_{1}^{0} + X_{soft}"
    #     branching="#tilde{#chi}_{1}^{0} #rightarrow H #tilde{G} (50%)";
    #     lightSq="#tilde{#chi}_{1}^{0} #rightarrow Z #tilde{G} (50%) ";
        


    if model=="T2tt":
#        branching = "BR(LQ #rightarrow t #nu) = 100%"
        branching = "#it{B}(LQ #rightarrow t #nu) = 1-#beta"
    elif model=="T2bb":
        branching = "#it{B}(LQ #rightarrow b #nu) = 100%"
    elif model=="T2qq":
        branching = "#it{B}(LQ #rightarrow q #nu) = 100%"
        lightSq = "(q = u, d, s, or c)"
#        lightSq = "(q = u, d, s)"
#        lightSq = "(q = c)"


    ROOT.gStyle.SetPaintTextFormat("4.3f");
    ROOT.gStyle.SetOptStat(0)
    c1 = ROOT.TCanvas("c1", "", 800, 700)
#    c1 = ROOT.TCanvas("c1", "", 800, 800)
    c1.cd()
    padt = ROOT.TPad("p_tex", "p_tex", 0.0, 0.0, 1.0, 1.0)
    padt.SetTopMargin(0.07)
    padt.SetBottomMargin(0.14)
    padt.SetRightMargin(0.05)
    padt.SetLeftMargin(0.12)


    # padt.SetTopMargin(0.1)
    # padt.SetBottomMargin(0.1)
    # padt.SetRightMargin(0.05)
    # padt.SetLeftMargin(0.15)

#    padt.SetTickx()
#    padt.SetTicky()
    padt.Draw()
    padt.cd()
    padt.SetLogy() 
    
    h = ROOT.TH2F()
#    if model=="T2tt":
#        h = ROOT.TH2F("h","h", nbins, xmin, xmax, 1000,0.5e-3,5000)
#    elif model=="T2bb":
#        h = ROOT.TH2F("h","h", nbins, xmin, xmax, 1000,0.5e-3,50)
#    elif model=="T2qq":
#        h = ROOT.TH2F("h","h", nbins, xmin, xmax, 1000,0.5e-3,100)
#    h = ROOT.TH2F("h","h", nbins, xmin, xmax, 1000,0.25e-3,10000)


    plotYmin = 0.1-0.01
    #    plotYmin = 0.09
    if model=="HZ":
        plotYmin = 0.1

    ROOT.gStyle.SetLabelSize(.05, "XY");

    h = ROOT.TH2F("h","h", nbins, 125, 450, 1000,plotYmin,1000)
#    h = ROOT.TH2F("h","h", nbins, 125, 400, 1000,0,10)
#    h = ROOT.TH2F("h","h", nbins, plotYmin, xmax, 1000,0,10)
    h.SetTitle("")
#    h.GetXaxis().SetTitle("m_{#chi_{1}^{0}} [GeV]")
    h.GetXaxis().SetTitle("Higgsino mass m_{#tilde{#chi}^{0}_{1}} [GeV]") 
#    h.GetYaxis().SetTitle("95% CL upper limit on cross section [pb]")
#    h.GetYaxis().SetTitle("#sigma  [pb]")
    h.GetYaxis().SetTitle("#sigma^{95%}_{excl} [pb]")
    #h.GetYaxis().CenterTitle(True)

#    h.GetXaxis().SetLabelOffset(0.003)

    h.GetXaxis().SetNdivisions(509)
#    h.GetXaxis().SetLabelSize(0.04)
#    h.GetXaxis().SetLabelSize(0.035)
 #   h.GetYaxis().SetLabelSize(0.04)
#    h.GetYaxis().SetLabelSize(0.035)
    h.GetXaxis().SetTitleSize(0.05)
    h.GetYaxis().SetTitleSize(0.05)
 #   h.GetXaxis().SetTitleOffset(0.95)

    h.GetXaxis().SetTitleSize(0.05);
    h.GetXaxis().SetLabelOffset( 0.003);
    h.GetYaxis().SetLabelOffset( 0.003);
    h.GetXaxis().SetTitleOffset( 1.2);
    h.GetYaxis().SetTitleOffset( 0.99);

#    h.GetYaxis().SetTitleOffset(0.8)
#    h.GetXaxis().SetLabelOffset(0.003)
#    h.GetYaxis().SetLabelOffset(0.003)
#    h.GetYaxis().SetTitleOffset(0.99)

    # h.GetXaxis().SetNdivisions(509)
    # h.GetXaxis().SetLabelSize(0.04)
    # h.GetXaxis().SetLabelSize(0.035)
    # h.GetYaxis().SetLabelSize(0.04)
    # h.GetYaxis().SetLabelSize(0.035)
    # h.GetXaxis().SetTitleSize(0.042)
    # h.GetYaxis().SetTitleSize(0.042)
    # h.GetXaxis().SetTitleSize(0.047)
    # h.GetYaxis().SetTitleSize(0.047)
    # h.GetXaxis().SetTitleOffset(1.0)
    # h.GetYaxis().SetTitleOffset(1.5)

    h.Draw()
    
    gr_s2b = ROOT.TGraphAsymmErrors(len(mass),array.array('d', mass),array.array('d', exp),array.array('d', x0e),array.array('d', x0e),array.array('d', m2s),array.array('d', p2s))
    gr_s2b.SetFillColor(ROOT.kOrange)
    gr_s2b.SetLineColor(0)
    gr_s2b.Draw("3")
      
    gr_s1b = ROOT.TGraphAsymmErrors(len(mass),array.array('d', mass),array.array('d', exp),array.array('d', x0e),array.array('d', x0e),array.array('d', m1s),array.array('d', p1s))
    gr_s1b.SetFillColor(ROOT.kGreen+1)
    gr_s1b.SetLineColor(0)
    gr_s1b.Draw("3")
    
    gexp = ROOT.TGraph(len(mass), array.array('d', mass), array.array('d', exp))
    gexp.SetLineStyle(7)
    gexp.SetLineWidth(3)
    gexp.SetLineColor(ROOT.kBlack)
    gexp.Draw("L")
    
    gsigmas = ROOT.TGraph(len(mass), array.array('d', mass), array.array('d', sigmas))
    gsigmas.SetLineStyle(7)
    gsigmas.SetLineWidth(3)
    gsigmas.SetLineColor(ROOT.kRed)

    g_xsec_slq.SetFillColor(ROOT.kBlue)
    g_xsec_slq.SetLineColor(ROOT.kBlue)
    g_xsec_slq.SetLineWidth(2)
    g_xsec_slq.Draw("L same")

    g_xsec_slqU.SetFillColor(ROOT.kBlue)
    g_xsec_slqU.SetLineColor(ROOT.kBlue)
    g_xsec_slqU.SetLineStyle(2)
    g_xsec_slqU.SetLineWidth(2)
    g_xsec_slqU.Draw("L same")

    g_xsec_slqD.SetFillColor(ROOT.kBlue)
    g_xsec_slqD.SetLineColor(ROOT.kBlue)
    g_xsec_slqD.SetLineStyle(2)
    g_xsec_slqD.SetLineWidth(2)
    g_xsec_slqD.Draw("L same")


    g_xsec_slq.SetFillColor(ROOT.kRed)
    g_xsec_slq.SetLineColor(ROOT.kRed)
    g_xsec_slq.SetLineWidth(3)
    g_xsec_slq.Draw("L same")

    g_xsec_slqU.SetFillColor(ROOT.kRed)
    g_xsec_slqU.SetLineColor(ROOT.kRed)
    g_xsec_slqU.SetLineStyle(2)
    g_xsec_slqU.SetLineWidth(3)
    g_xsec_slqU.Draw("L same")

    g_xsec_slqD.SetFillColor(ROOT.kRed)
    g_xsec_slqD.SetLineColor(ROOT.kRed)
    g_xsec_slqD.SetLineStyle(2)
    g_xsec_slqD.SetLineWidth(3)
    g_xsec_slqD.Draw("L same")
     

    gobs = ROOT.TGraph(len(mass), array.array('d', mass), array.array('d', obs))
    gobs.SetMarkerStyle(ROOT.kFullCircle)
    gobs.SetMarkerSize(1.5)
    gobs.SetMarkerColor(ROOT.kBlack)
    gobs.SetLineWidth(3)
    gobs.SetLineColor(ROOT.kBlack)
    gobs.Draw("L")
   
#    prctex = ROOT.TLatex(0.21,0.83, ppSqSq );
    prctex = ROOT.TLatex(0.15,0.87, ppSqSq );
    prctex.SetNDC()    
    prctex.SetTextSize(0.048)    
    prctex.SetLineWidth(2)
    prctex.SetTextFont(42)    
    prctex.Draw()

#    prctex2 = ROOT.TLatex(0.21,0.78, branching );    

    cmsxlabel = 0.29+0.263 -0.10
    cmsylabel = 0.88-0.07-0.02

    if model=="HZ":
        cmsxlabel = 0.29+0.415- 0.05
        cmsylabel = 0.88-0.07-0.02       

    prctex2 = ROOT.TLatex(cmsxlabel,cmsylabel, branching );    
    prctex2.SetNDC()    
    prctex2.SetTextSize(0.048)    
    prctex2.SetLineWidth(2)
    prctex2.SetTextFont(42)    
    prctex2.Draw()

    if model=="HZ":
#        prctex3 = ROOT.TLatex(0.21,0.73, lightSq );
        prctex3 = ROOT.TLatex(0.29+0.25-0.1,0.87-0.13-0.01, lightSq );
        prctex3.SetNDC()    
        prctex3.SetTextSize(0.048)    
        prctex3.SetLineWidth(2)
        prctex3.SetTextFont(42)    
        prctex3.Draw()


#    cmstex = ROOT.TLatex(0.675,0.91, "%.1f fb^{-1} (13 TeV)" % lumi)
    cmstex = ROOT.TLatex(0.955,0.945, "%.1f fb^{-1} (13 TeV)" % lumi)
    cmstex.SetNDC()
    cmstex.SetTextSize(0.06)
    cmstex.SetLineWidth(2)
    cmstex.SetTextFont(42)
    cmstex.SetTextAlign(31)
    cmstex.Draw()
    
#    cmstexbold = ROOT.TLatex(0.15,0.91, "CMS" )
    cmstexbold = ROOT.TLatex(0.25,0.94, "CMS" )
    cmstexbold.SetNDC()
#    cmstexbold.SetTextSize(0.05)
    cmstexbold.SetTextSize(0.06)
    cmstexbold.SetLineWidth(2)
    cmstexbold.SetTextFont(61)
    cmstexbold.SetTextAlign(31)
    cmstexbold.Draw()
    
    cmstexprel = ROOT.TLatex(0.45,0.94, "Preliminary" )
    cmstexprel.SetNDC()
    cmstexprel.SetTextAlign(31)
    cmstexprel.SetTextSize(0.76*0.06)
    cmstexprel.SetLineWidth(2)
    cmstexprel.SetTextFont(52)
#    cmstexprel.Draw()


    H = padt.GetWh()
    W = padt.GetWw()
    l = padt.GetLeftMargin()
    t = 0.07
    r = 0.05
    b = padt.GetBottomMargin()
    e = 0.025

#    writeAnalysisText = True
    analysisText   = "#bf{SP analysis}"
#    analysisText   = "#bf{STP Analysis}"
    analysisTextFont = 42 
    lumiTextSize     = 0.6
    lumiTextOffset   = 0.2
    
#    l1 = ROOT.TLegend(0.51, 0.48-0.09, 0.78, 0.87)
#    l1 = ROOT.TLegend(0.51, 0.48-0.09, 0.78, 0.8)
    l1 = ROOT.TLegend(0.51, 0.75-5*0.065-0.02+0.01, 0.85, 0.75-0.05-0.02)
#TLegend* leg = new TLegend( 0.51, 0.75-5*0.065-0.02, 0.85, 0.75-0.05-0.02, NULL, "brNDC" );
    l1.SetFillStyle(1001) 
    l1.SetLineColor(1)
    l1.SetBorderSize(0)

    l1.SetTextFont(41)
    l1.SetTextSize(0.04)
    l1.SetLineColor(ROOT.kWhite)
    l1.SetShadowColor(ROOT.kWhite)
    l1.SetFillColor(ROOT.kWhite)

    theoryText = "NLO+NLL theory"

    l1.AddEntry(g_xsec_slq , theoryText,"l")
#    l1.AddEntry(g_xsec_slq , " #sigma_{theory, NLO} ","l")
    l1.AddEntry(gobs , "Observed limit (95% CL)", "l")
    l1.AddEntry(gexp , "Median expected limit", "l")
    l1.AddEntry(gr_s1b , "68% expected", "f")
    l1.AddEntry(gr_s2b , "95% expected", "f")

  #   if model!="T2tt":
#         l1.AddEntry(g_xsec_vlq , "#sigma_{theory, LO}^{pp #rightarrow LQ_{V} LQ_{V}} (#kappa=1)","l")
#         l1.AddEntry(g_xseck0_vlq , "#sigma_{theory, LO}^{pp #rightarrow LQ_{V} LQ_{V}} (#kappa=0)","l")
#         l1.AddEntry(g_xsec_slq , "#sigma_{theory, NLO}^{pp #rightarrow LQ_{S} LQ_{S}}","l")
#     if model=="T2tt":
#         l1.AddEntry(g_xsec_vlq , "#sigma_{theory, LO}^{pp #rightarrow LQ_{V} LQ_{V}} (#kappa=1; #beta=0)","l")
#         l1.AddEntry(g_xsec0p25_vlq , "#sigma_{theory, LO}^{pp #rightarrow LQ_{V} LQ_{V}} (#kappa=1; #beta=0.5)","l")
#         l1.AddEntry(g_xseck0_vlq , "#sigma_{theory, LO}^{pp #rightarrow LQ_{V} LQ_{V}} (#kappa=0; #beta=0)","l")
# #        l1.AddEntry(g_xseck0_0p25_vlq , "#sigma_{theory, LO}^{pp #rightarrow LQ_{V} LQ_{V}} (#kappa=0; #beta=0.5)","l")
#         l1.AddEntry(g_xsec_slq , "#sigma_{theory, NLO}^{pp #rightarrow LQ_{S} LQ_{S}} (#beta=0)","l")

 
    l1.Draw()


    latex0 = ROOT.TLatex(0.42,1-5*0.07,    analysisText)
    latex0.SetNDC()
#    latex0.SetTextColor(ROOT.kBlack)    
    latex0.SetTextFont(42)
    latex0.SetTextAlign(31) 
    latex0.SetTextSize( 0.05)
    #latex0.DrawLatex(1-3.1*r,1-5*t,analysisText)
    latex0.Draw()

    '''
    LExp1 = ROOT.TGraphAsymmErrors(2)
    LExp1.SetFillColor(ROOT.kOrange)
    LExp1.SetPoint(0,250+100000,100000)
    LExp1.SetPointError(0,0.,0.,0.1,50.15)
    LExp1.SetPoint(1,100000, 100000)
    LExp1.SetPointError(1,0.,0.,0.15,0.15)
    LExp1.Draw("3")
    
    LExp2 = ROOT.TGraphAsymmErrors(2)
    LExp2.SetFillColor(ROOT.kGreen+1)
    LExp2.SetPoint(0,100000,100000)
    LExp2.SetPointError(0,0.,0.,0.08,0.08)
    LExp2.SetPoint(1,100000,100000)
    LExp2.SetPointError(1,0.,0.,0.08,0.08)
    LExp2.Draw("L3")
    
    LExp = ROOT.TGraph(2)
    LExp.SetLineColor(ROOT.kBlack)
    LExp.SetLineStyle(7)
    LExp.SetLineWidth(3)
    LExp.SetPoint(0,250+ 3.8*(1050-250)/100, 5-2.08*(5-0)/100*10)
    LExp.SetPoint(1,250+21.2*(1050-250)/100, 5-2.08*(5-0)/100*10)
    LExp.Draw("L")
    ''' 
    
    if model=="T2tt":
        svU = ROOT.TGraph()
        svU.SetLineColor(ROOT.kRed)
        svU.SetLineStyle(2)
        svU.SetLineWidth(2)
#        svU.SetPoint(0,1230, 10.2)
#        svU.SetPoint(1,1340, 10.2)
        svU.SetPoint(0,1230, 11.75)
        svU.SetPoint(1,1340, 11.75)
        svU.Draw("L")
        svD = ROOT.TGraph()
        svD.SetLineColor(ROOT.kRed)
        svD.SetLineStyle(2)
        svD.SetLineWidth(2)
#        svD.SetPoint(0,1230, 5.5)
#        svD.SetPoint(1,1340, 5.5)
        svD.SetPoint(0,1230, 7.75)
        svD.SetPoint(1,1340, 7.75)
        svD.Draw("L")
        
        sv0p25U = ROOT.TGraph()
        sv0p25U.SetLineColor(ROOT.kMagenta-7)
        sv0p25U.SetLineStyle(2)
        sv0p25U.SetLineWidth(2)
#        sv0p25U.SetPoint(0,1230, 2.4)
#        sv0p25U.SetPoint(1,1340, 2.4)
        sv0p25U.SetPoint(0,1230, 2.9)
        sv0p25U.SetPoint(1,1340, 2.9)
        sv0p25U.Draw("L")    
        sv0p25D = ROOT.TGraph()
        sv0p25D.SetLineColor(ROOT.kMagenta-7)
        sv0p25D.SetLineStyle(2)
        sv0p25D.SetLineWidth(2)
#        sv0p25D.SetPoint(0,1230, 1.55)
#        sv0p25D.SetPoint(1,1340, 1.55)
        sv0p25D.SetPoint(0,1230, 1.9)
        sv0p25D.SetPoint(1,1340, 1.9)
        sv0p25D.Draw("L")
        
        svkU = ROOT.TGraph()
        svkU.SetLineColor(ROOT.kCyan+1)
        svkU.SetLineStyle(2)
        svkU.SetLineWidth(2)
        svkU.SetPoint(0,1230, 0.7)
        svkU.SetPoint(1,1340, 0.7)
        svkU.Draw("L")    
        svkD = ROOT.TGraph()
        svkD.SetLineColor(ROOT.kCyan+1)
        svkD.SetLineStyle(2)
        svkD.SetLineWidth(2)
        svkD.SetPoint(0,1230, 0.475)
        svkD.SetPoint(1,1340, 0.475)
        svkD.Draw("L")
        
        ssU = ROOT.TGraph()
        ssU.SetLineColor(ROOT.kBlue)
        ssU.SetLineStyle(2)
        ssU.SetLineWidth(2)
#        ssU.SetPoint(0,1230, 0.565)
#        ssU.SetPoint(1,1340, 0.565)
        ssU.SetPoint(0,1230, 0.175)
        ssU.SetPoint(1,1340, 0.175)
        ssU.Draw("L")    
        ssD = ROOT.TGraph()
        ssD.SetLineColor(ROOT.kBlue)
        ssD.SetLineStyle(2)
        ssD.SetLineWidth(2)
#        ssD.SetPoint(0,1230, 0.365)
#        ssD.SetPoint(1,1340, 0.365)
        ssD.SetPoint(0,1230, 0.115)
        ssD.SetPoint(1,1340, 0.115)
        ssD.Draw("L")
    
    else:
        svU = ROOT.TGraph()
        svU.SetLineColor(ROOT.kRed)
        svU.SetLineStyle(2)
        svU.SetLineWidth(2)
#        svU.SetPoint(0,1230, 11.0)
#        svU.SetPoint(1,1340, 11.0)
        svU.SetPoint(0,1230, 7.3)
        svU.SetPoint(1,1340, 7.3)
        svU.Draw("L")
        svD = ROOT.TGraph()
        svD.SetLineColor(ROOT.kRed)
        svD.SetLineStyle(2)
        svD.SetLineWidth(2)
#        svD.SetPoint(0,1230, 6.75)
#        svD.SetPoint(1,1340, 6.75)
        svD.SetPoint(0,1230, 5.0)
        svD.SetPoint(1,1340, 5.0)
        svD.Draw("L")
        
        svkU = ROOT.TGraph()
        svkU.SetLineColor(ROOT.kCyan+1)
        svkU.SetLineStyle(2)
        svkU.SetLineWidth(2)
#        svkU.SetPoint(0,1230, 2.65)
#        svkU.SetPoint(1,1340, 2.65)
        svkU.SetPoint(0,1230, 1.65)
        svkU.SetPoint(1,1340, 1.65)
        svkU.Draw("L")    
        svkD = ROOT.TGraph()
        svkD.SetLineColor(ROOT.kCyan+1)
        svkD.SetLineStyle(2)
        svkD.SetLineWidth(2)
#        svkD.SetPoint(0,1230, 1.65)
#        svkD.SetPoint(1,1340, 1.65)
        svkD.SetPoint(0,1230, 1.1)
        svkD.SetPoint(1,1340, 1.1)
        svkD.Draw("L")

        ssU = ROOT.TGraph()
        ssU.SetLineColor(ROOT.kBlue)
        ssU.SetLineStyle(2)
        ssU.SetLineWidth(2)
#        ssU.SetPoint(0,1230, 2.65)
#        ssU.SetPoint(1,1340, 2.65)
        ssU.SetPoint(0,1230, 0.37)
        ssU.SetPoint(1,1340, 0.37)
        ssU.Draw("L")    
        ssD = ROOT.TGraph()
        ssD.SetLineColor(ROOT.kBlue)
        ssD.SetLineStyle(2)
        ssD.SetLineWidth(2)
#        ssD.SetPoint(0,1230, 1.65)
#        ssD.SetPoint(1,1340, 1.65)
        ssD.SetPoint(0,1230, 0.245)
        ssD.SetPoint(1,1340, 0.245)
        ssD.Draw("L")

        
    ROOT.gPad.RedrawAxis()


    if model=="T2tt":
        c1.SaveAs("T2tt_1DExclusion_13TeV_NNPDF_fullrange_fV_k.pdf")
#        c1.SaveAs("T2tt_1DExclusion_13TeV_NNPDF_fullrange_fV_k_b0p5.pdf")
    elif model=="T2bb":
        c1.SaveAs("T2bb_1DExclusion_13TeV_NNPDF_fullrange_fV_k.pdf")
    elif model=="T2qq":
        c1.SaveAs("T2qq_1DExclusion_13TeV_NNPDF_fullrange_fV_k.pdf")
    elif model=="HH":
        c1.SaveAs("HH_1DExclusion_13TeV_aug13.pdf")
        c1.SaveAs("HH_1DExclusion_13TeV_aug13.png")
        c1.SaveAs("HH_1DExclusion_13TeV_aug13.C")
        c1.SaveAs("HH_1DExclusion_13TeV_aug13.root")
    elif model=="HZ":
        c1.SaveAs("HZ_1DExclusion_13TeV_aug13.pdf")
        c1.SaveAs("HZ_1DExclusion_13TeV_aug13.png")
        c1.SaveAs("HZ_1DExclusion_13TeV_aug13.C")
        c1.SaveAs("HZ_1DExclusion_13TeV_aug13.root")


    cmstexprel.Draw()

    if model=="HH":
        c1.SaveAs("HH_1DExclusion_13TeV_aug13_preliminary.pdf")
        c1.SaveAs("HH_1DExclusion_13TeV_aug13_preliminary.png")
        c1.SaveAs("HH_1DExclusion_13TeV_aug13_preliminary.C")
    elif model=="HZ":
        c1.SaveAs("HZ_1DExclusion_13TeV_aug13_preliminary.pdf")
        c1.SaveAs("HZ_1DExclusion_13TeV_aug13_preliminary.png")
        c1.SaveAs("HZ_1DExclusion_13TeV_aug13_preliminary.C")



    ### store histogram versions of limits
    f_out = ROOT.TFile("limits_"+model+"_NNPDF_fullrange_fV_aux_k.root","RECREATE")
    f_out.cd()
    g_xsec_slq.Write("g_xsec_slq")

    g_xsec_slqU.Write("g_xsec_slqU")
    g_xsec_slqD.Write("g_xsec_slqD")

    # g_xsec_vlq.Write("g_xsec_vlq")
    # g_xsec_vlqU.Write("g_xsec_vlqU")
    
    # g_xsec_vlqD.Write("g_xsec_vlqD")
    # g_xsec0p25_vlq.Write("g_xsec0p25_vlq")
    # g_xsec0p25_vlqU.Write("g_xsec0p25_vlqU")
    # g_xsec0p25_vlqD.Write("g_xsec0p25_vlqD")
    # g_xseck0_vlq.Write( "g_xseck0_vlq")
    # g_xseck0_vlqU.Write("g_xseck0_vlqU")
    # g_xseck0_vlqD.Write("g_xseck0_vlqD")
    # g_xseck0_0p25_vlq.Write( "g_xseck0_0p25_vlq")
    # g_xseck0_0p25_vlqU.Write("g_xseck0_0p25_vlqU")
    # g_xseck0_0p25_vlqD.Write("g_xseck0_0p25_vlqD")

    gexp.SetName("graphExp")
    gexp.SetTitle("TGraph for median expected limit")
    gexp.SetLineColor(1)
    gexp.SetLineStyle(1)
    gexp.SetMarkerStyle(4)
    gexp.SetMarkerColor(1)
    gexp.Write()


    gobs.SetName("graphObs")
    gobs.SetTitle("TGraph for observed limit (95% CL)")
    gobs.SetLineColor(1)
    gobs.SetLineStyle(1)
    gobs.SetMarkerStyle(4)
    gobs.SetMarkerColor(1)
    gobs.Write()

    gr_s1b.SetName("graphExp1S")
    gr_s1b.SetTitle("TGraphAsymmError for 68% expected band")
    gr_s1b.SetLineColor(1)
    gr_s1b.SetLineStyle(1)
    gr_s1b.SetMarkerStyle(4)
    gr_s1b.SetMarkerColor(1)
    gr_s1b.Write()
    gr_s2b.SetName("graphExp2S")
    gr_s2b.SetTitle("TGraphAsymmError for 95% expected band")
    gr_s2b.SetLineColor(1)
    gr_s2b.SetLineStyle(1)
    gr_s2b.SetMarkerStyle(4)
    gr_s2b.SetMarkerColor(1)
    gr_s2b.Write()
    
    f_out.Close()


#####################################################################################################
if __name__ == "__main__":
    main()
