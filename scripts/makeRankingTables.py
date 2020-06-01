import os
import sys

# directory to cross section
xsecFileName="/shome/casal/SUSxsecs/SUSYCrossSections13TeV"
# path to full table
fulltable = open("/mnt/t3nfs01/data01/shome/casal/CMSSW_7_4_12_patch4_MT2/src/analysisJul/analysis/latexBGTable_EventYields_data_Run2016_7p7ifb.tex", "r")



if len(sys.argv)<3:
    print "Usage: "+sys.argv[0]+" model lumi(fb) [limits.txt]"
    exit(1)

modelpoint = str  (sys.argv[1])
model = modelpoint.split("_")[0]
m1    = modelpoint.split("_")[1]
m2    = modelpoint.split("_")[2]

lumi  = float(sys.argv[2])

obs, exp = "xxx", "yyy"
if len(sys.argv) >3:
    limits = open(sys.argv[3] , "r").readlines()
    for l in limits:
        if l.split()[0]==m1 and l.split()[1]==m2:
            exp = l.split()[2]
            obs = l.split()[3]    


if "T1" in modelpoint:
    xsecFileName=xsecFileName+"gluglu.txt"
elif "T2qq" in modelpoint:
    xsecFileName=xsecFileName+"squarkantisquark.txt"
else:
    xsecFileName=xsecFileName+"stopstop.txt"

xsecFile = open(xsecFileName, "r")

xsec=1.0;
xsecs = xsecFile.readlines()
for l in xsecs:
    if l.split()[0]==m1:
        xsec = float(l.split()[2])
        if "T2qq" in modelpoint:
            xsec=float(xsec)*1./10.
        break


htregions={
"HT200to450": "$200 < $H$_{\mathrm{T}} < 450$~GeV",
"HT450to575": "$450 < $H$_{\mathrm{T}} < 575$~GeV",
"HT575to1000": "$575 < $H$_{\mathrm{T}} < 1000$~GeV",
"HT1000to1500": "$1000 < $H$_{\mathrm{T}} < 1500$~GeV",
"HT1500toInf": "H$_{\mathrm{T}} > 1500$~GeV",
"HT200to250": "$200 < $H$_{\mathrm{T}} < 250$~GeV",
"HT250to350": "$250 < $H$_{\mathrm{T}} < 350$~GeV",
"HT350to450": "$350 < $H$_{\mathrm{T}} < 450$~GeV",
"HT575toInf": "H$_{\mathrm{T}} > 575$~GeV",
"HT575to700": "$575 < $H$_{\mathrm{T}} < 700$~GeV",
"HT700to1000": "$700 < $H$_{\mathrm{T}} < 1000$~GeV",
"HT1000toInf": "H$_{\mathrm{T}} > 1000$~GeV"
}

jetregions={
"j1": "$1$j",
"j2to3": "$2-3$j",
"j4to6": "$4-6$j",
"j7toInf": "$\geq7$j",
"j2to6": "$2-6$j",
}

btagregions={
"b0": "$0$b",
"b1": "$1$b",
"b2": "$2$b",
"b3toInf": "$\geq3$b",
"b1toInf": "$\geq1$b"
}

postfitline = "Total (post-fit)"
obsline = "Observation"
mt2line = "Process"

fulllines = fulltable.readlines()

observation={}
postfit={}
fullmt2bin={}

htregion, jetregion, btagregion = "", "", ""
for l in fulllines:
    if "caption" in l:
        for ht in htregions:
            if htregions[ht] in l:
                htregion=ht
                break
        for nj in jetregions:
            if jetregions[nj] in l:
                jetregion=nj
                break
        for nb in btagregions:
            if btagregions[nb] in l:
                btagregion=nb
                break

    if "j1" in jetregion:
        fullmt2bin[htregion+'_'+jetregion+'_'+btagregion]=['m0toInf']
    
    if mt2line in l and "j1" not in jetregion:    
        fullmt2bin[htregion+'_'+jetregion+'_'+btagregion]=l.strip(' \\').strip(' \\\n').replace(" ", "").split('&')[1:]
    
    if postfitline in l:
        postfit[htregion+'_'+jetregion+'_'+btagregion]=l.strip(' \\').strip(' \\\n').replace(" ", "").split('&')[1:]
    
    if obsline in l:
        observation[htregion+'_'+jetregion+'_'+btagregion]=l.strip(' \\').strip(' \\\n').replace(" ", "").split('&')[1:]

tabmt2bin = {}
for r in fullmt2bin:
    if r not in tabmt2bin:
        tabmt2bin[r]=[]
    if "j1" not in r:
        for b, m in enumerate(fullmt2bin[r]):
            if "<$M$_{\mathrm{T2}}<" in fullmt2bin[r][b]:
                thisbin = 'm'+fullmt2bin[r][b].replace("<$M$_{\mathrm{T2}}<", "to").replace("$", "").replace("~GeV", "").strip(" ")
                tabmt2bin[r].append(thisbin)
            else:
                thisbin = 'm'+fullmt2bin[r][b].replace("M$_{\mathrm{T2}}>", "").replace("$", "").replace("~GeV", "").strip(" ")+'toInf'
                tabmt2bin[r].append(thisbin)
    else:
        tabmt2bin[r] = fullmt2bin[r]

postfitdic, observationdic = {}, {}
for r in tabmt2bin:
    postfitdic[r]    =dict(zip(tabmt2bin[r], postfit[r]))
    observationdic[r]=dict(zip(tabmt2bin[r], observation[r]))

bintable = open("AsymptoticRanking_"+modelpoint+"_Paper_post_plusBG.txt", "r")
binlines = bintable.readlines()

mt2bin, sigyield, bgyield = {}, {}, {}

for l in binlines:
    if 'HT' in l:
        region=l.strip('\n')
    else:
        if region not in mt2bin:
            mt2bin[region], sigyield[region], bgyield[region]=[],[],[]
        mt2bin  [region].append(l.strip(' \\').strip(' \\\n').replace(" ", "").split('&')[0])
        sigyield[region].append(l.strip(' \\').strip(' \\\n').replace(" ", "").split('&')[1])
        bgyield [region].append(l.strip(' \\').strip(' \\\n').replace(" ", "").split('&')[2])
        

rankedtable = open("AsymptoticRanking_"+modelpoint+"_Paper_post_ranked.txt", "r")
rankedlines = rankedtable.readlines()

explim, obslim, totalsig, acceptance = {}, {}, {}, {}

table_body = ""

for nl, l in enumerate(rankedlines):
    region=l.strip(' \\').strip(' \\\n').replace(" ", "").split('&')[0]
    if region not in explim:
        explim[region], obslim[region], totalsig[region], acceptance[region] = [], [], [], []
    if nl<10:
        explim[region]     = l.strip(' \\').strip(' \\\n').replace(" ", "").split('&')[1]
        obslim[region]     = l.strip(' \\').strip(' \\\n').replace(" ", "").split('&')[2]
        totalsig[region]   = l.strip(' \\').strip(' \\\n').replace(" ", "").split('&')[3]
        acceptance[region] = l.strip(' \\').strip(' \\\n').replace(" ", "").split('&')[4] # assumes 1/fb
        acceptance[region] = "%.3f" % (float(acceptance[region])/lumi)  #correct acceptance by real lumi
        
        table_body += region.replace("_", " ") + ' & ' + explim[region] + ' & ' + obslim[region] + ' & ' + totalsig[region] + ' & ' + acceptance[region] + ' & ' + mt2bin[region][0] + ' & '+ sigyield[region][0]+ ' & ' + bgyield[region][0] + ' & ' + postfitdic[region][mt2bin[region][0]] + ' & ' + observationdic[region][mt2bin[region][0]] + ' \\\\\n'
        for m, mt2 in enumerate(mt2bin[region]):
            if m>0:
                table_body += '& & & & & '+ mt2bin[region][m] + ' & ' + sigyield[region][m] + ' & ' + bgyield[region][m] + ' & ' + postfitdic[region][mt2] + ' & ' + observationdic[region][mt2] + ' \\\\\n'
        table_body += "\\hline\n"

table_begin = '''\\begin{{table}}[htbp]
\\caption{{{model} ({m1}, {m2}): ranking of topological regions, according to expected exclusion limit, foran integrated luminosity of {lumi}~fb$^{{-1}}$. Cross-section: {xsec}~pb. Expected exclusion limit: {exp}. Observed exclusion limit: {obs}.}}
\\scriptsize
\\centering
\\makebox[\\textwidth][c]{{
\\begin{{tabular}}{{|r|c|c|c|c|r|c|c|c|c|}}
\\hline
\\hline
Region &  Exp. Limit & Obs. Limit & Signal Yield & Acceptance (\%)  & $M_{{\mathrm{{T2}}}}$ & Signal & SM (pre-fit) & SM (post-fit) & Observation\\\\
\\hline
\\hline
'''.format(model=model, m1=m1, m2=m2, lumi=lumi, xsec=xsec, exp=exp, obs=obs)


table_end = '''\hline
\end{tabular}}
\end{table}
'''


print table_begin, table_body, table_end

#for r in explim:
#    if r in mt2bin:
#        print r, tabmt2bin[r], postfit[r], observation[r], mt2bin[r], sigyield[r], bgyield[r]
#        print explim[r], obslim[r]
#        #print r, postfit[r], observation[r], mt2bin[r], sigyield[r], bgyield[r]
#        print "WARNING!!!!!!" if len(mt2bin[r]) < len(postfit[r]) else ""
    

#
#
#
#output=open('/shome/mmasciov/latex/'+modelpoint+'_ranking.txt', 'w+')
