import ROOT, sys, collections, math

# Set ATLAS style
def setATLASStyle(path="/afs/cern.ch/work/t/tvarol/bbyy_0917/scripts/createNewSampleDistr"):
    ROOT.gROOT.SetMacroPath(path)
    ROOT.gROOT.LoadMacro("AtlasStyle.C")
    ROOT.gROOT.LoadMacro("AtlasLabels.C")
    ROOT.gROOT.LoadMacro("AtlasUtils.C")
    ROOT.SetAtlasStyle() 

def compareHistograms(f0,f1,f2,histo="m_yy",rebin=1):
    h0 = f0.Get(histo)
    h0_tot = f0.Get("afterParSel")
    h1 = f1.Get(histo)
    h1_tot = f1.Get("afterParSel")
    h2 = f2.Get(histo)
    h2_tot = f2.Get("afterParSel")
    h0.Scale(float(lamb['0'])*pow(10,-3)/h0_tot.Integral())
    h1.Scale(float(lamb['1'])*pow(10,-3)/h1_tot.Integral())
    h2.Scale(float(lamb[str(int(smpl))])*pow(10,-3)/h2_tot.Integral())
    if int(smpl)==2:
        err = ROOT.Double()
        h0.Scale((1+(0.5*pow(float(kl),2))-1.5*float(kl)))
        val = h0.IntegralAndError(0,-1,err)
        if "mass_bbyy_1t_l" in h0.GetName():
            print('1: %.4f +/- %.4f'%(val,err))
        h0.Add(h1, (2*float(kl)-(pow(float(kl),2))))
        val = h0.IntegralAndError(0,-1,err)
        if "mass_bbyy_1t_l" in h0.GetName():
            print('2: %.4f +/- %.4f'%(val,err))
        h0.Add(h2, 0.5*(pow(float(kl),2)-float(kl)))
        val = h0.IntegralAndError(0,-1,err)
        if "mass_bbyy_1t_l" in h0.GetName():
            print('3: %.4f +/- %.4f'%(val,err))
    elif int(smpl)==10:
	err = ROOT.Double()
        h0.Scale( 1 + (0.1*pow(float(kl),2)) - (99*float(kl)*(1./90.)) )
	val = h0.IntegralAndError(0,-1,err)
	if "mass_bbyy_1t_l" in h0.GetName():
		print('1: %.4f +/- %.4f'%(val,err))
        h0.Add(h1, ( (100*float(kl) - 10*pow(float(kl),2))*(1./90.)) )
	val = h0.IntegralAndError(0,-1,err)
	if "mass_bbyy_1t_l" in h0.GetName():
		print('2: %.4f +/- %.4f'%(val,err))
        h0.Add(h2, ((pow(float(kl),2) - float(kl))*(1./90.)) )
	val = h0.IntegralAndError(0,-1,err)
	if "mass_bbyy_1t_l" in h0.GetName():
		print('3: %.4f +/- %.4f'%(val,err))
    elif int(smpl)==20:
        h0.Scale( 1 + (19*pow(float(kl),2)*(1./380.)) - (399*float(kl)*(1./380.)) )
        h0.Add(h1, ( (400*float(kl) - 20*pow(float(kl),2))*(1./380.)) )
        h0.Add(h2, ((pow(float(kl),2) - float(kl))*(1./380.)) )
    h0.Rebin(rebin) 
    return h0

kl = sys.argv[1]
smpl = sys.argv[2]

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
histList=['m_bb', 'm_yy', 'm_yybb']
xTitle=['m_{bb} [GeV]', 'm_{#gamma#gamma} [GeV]', 'm_{#gamma#gammabb} [GeV]']
rebin=[1,1,5]


lamb = {'-20':2138.2*7.85*pow(10,-3)*0.34, '-10':6.597*0.78397*0.34, '-6':3.061*0.78192*0.34, '-4':1.802*0.78127*0.34, '-2':88.33*7.8553*pow(10,-3)*0.34, "-1":55.22*7.8391*pow(10,-3)*0.34, "0":30.56*7.8677*pow(10,-3)*0.34, "1":14.42*7.8752*pow(10,-3)*0.34, "2":6.758*7.8518*pow(10,-3)*0.34, "4":16.96*7.8450*pow(10,-3)*0.34, "6":61.17*7.8599*pow(10,-3)*0.34, "10":2.515*0.78568*0.34, "20":1322.1*7.85*pow(10,-3)*0.34}

outdir = "combinedFiles/"

if float(kl)>1:
    if (float(kl)*10)%10==0:
        outFileName = "hist-SM%sp.root"%(kl)
    else:
        outFileName = "hist-SM%sp.root"%(float(kl))
elif float(kl)<0:
    if (float(kl)*10)%10==0:
        outFileName = "hist-SM%sm.root"%(abs(int(kl)))
    else:
        outFileName = "hist-SM%sm.root"%(abs(float(kl)))

print "Output name = %s"%(outFileName) 
output = ROOT.TFile(outdir+outFileName, "RECREATE")

output.cd();
for idx,hist in enumerate(histList):
    hCalc = compareHistograms(f0,f1,f2,hist,rebin[idx])
    hCalc.Write()

output.Close()
