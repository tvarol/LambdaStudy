import ROOT, sys, collections, math

# Set ATLAS style
def setATLASStyle(path="/afs/cern.ch/work/t/tvarol/bbyy_0917/scripts/createNewSampleDistr"):
    ROOT.gROOT.SetMacroPath(path)
    ROOT.gROOT.LoadMacro("AtlasStyle.C")
    ROOT.gROOT.LoadMacro("AtlasLabels.C")
    ROOT.gROOT.LoadMacro("AtlasUtils.C")
    ROOT.SetAtlasStyle() 

def combineHistograms(f0,f1,f2,histo="m_yy",rebin=1,kl=15):
    h0 = f0.Get(histo).Clone()
    h0_tot = f0.Get("afterParSel").Clone()
    h1 = f1.Get(histo).Clone()
    h1_tot = f1.Get("afterParSel").Clone()
    h2 = f2.Get(histo).Clone()
    h2_tot = f2.Get("afterParSel").Clone()
    h0.Scale((float(lamb['0'])*pow(10,-3)*0.34)/h0_tot.Integral())
    h1.Scale((float(lamb['1'])*pow(10,-3)*0.34)/h1_tot.Integral())
    h2.Scale((float(lamb[str(int(smpl))])*pow(10,-3)*0.34)/h2_tot.Integral())
    
    if int(smpl)==2:
        h0.Scale((1+(0.5*pow(float(kl),2))-1.5*float(kl)))
        h0.Add(h1, (2*float(kl)-(pow(float(kl),2))))
        h0.Add(h2, 0.5*(pow(float(kl),2)-float(kl)))
    elif int(smpl)==10:
        h0.Scale( 1 + (0.1*pow(float(kl),2)) - (99*float(kl)*(1./90.)) )
        h0.Add(h1, ( (100*float(kl) - 10*pow(float(kl),2))*(1./90.)) )
        h0.Add(h2, ((pow(float(kl),2) - float(kl))*(1./90.)) )
    elif int(smpl)==20:
        h0.Scale( 1 + (19*pow(float(kl),2)*(1./380.)) - (399*float(kl)*(1./380.)) )
        h0.Add(h1, ( (400*float(kl) - 20*pow(float(kl),2))*(1./380.)) )
        h0.Add(h2, ((pow(float(kl),2) - float(kl))*(1./380.)) )

    h0.Rebin(rebin)
    h1.Rebin(rebin)  
    h0.Divide(h1)
    
    if float(kl)>1:                                                                                                            
        if (float(kl)*10)%10==0:                                                                                               
            histName = "_%sp"%(kl)                                                                                     
        else:                                                                                                       
            histName = "_%sp"%(float(kl))                                                                             
    elif float(kl)<0:                                                                                                   
        if (float(kl)*10)%10==0:                                                                                    
            histName = "_%sm"%(abs(int(kl)))                                                                        
        else:                                                                                                                
         histName = "_%sm"%(abs(float(kl)))
    elif float(kl)==0:
        histName = "_0"
    elif float(kl)==1:
        histName = "_1p"
    h0.SetName(histo+histName)
    return h0

smpl = sys.argv[1]
lambdas = [-25, -20, -15, -10, -9, -8, -7, -6, -5, -4, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25]

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetErrorX(0)
setATLASStyle()

f0 = ROOT.TFile.Open("hist-SM0.root")
f1 = ROOT.TFile.Open("hist-SM.root")
if int(smpl)==2:
    testFileName = "hist-SM2p.root"
elif int(smpl)==10:
    testFileName = "hist-SM10p.root"
elif int(smpl)==20:
    testFileName = "hist-SM20p.root"

print testFileName

f2 = ROOT.TFile.Open(testFileName)

histList=collections.OrderedDict()
xTitle=collections.OrderedDict()
rebinList=collections.OrderedDict()
histList=['m_yy', 'm_yybb']
xTitle=['m_{#gamma#gamma} [GeV]', 'm_{#gamma#gammabb} [GeV]']
rebinList=[1,10]

lamb = {'-20':2138.2*7.85*pow(10,-3), '-10':6.597*0.78397, '-6':3.061*0.78192, '-4':1.802*0.78127, '-2':88.33*7.8553*pow(10,-3), "-1":55.22*7.8391*pow(10,-3), "0":30.56*7.8677*pow(10,-3), "1":14.42*7.8752*pow(10,-3), "2":6.758*7.8518*pow(10,-3), "4":16.96*7.8450*pow(10,-3), "6":61.17*7.8599*pow(10,-3), "10":2.515*0.78568, "20":1322.1*7.85*pow(10,-3)}

output = ROOT.TFile("combinedFiles/allWeights.root", "RECREATE")

output.cd();

for newLambda in lambdas:
    for idx,hist in enumerate(histList):
        hCalc = combineHistograms(f0,f1,f2,hist,rebinList[idx],newLambda)
        hCalc.Write()

output.Close()
