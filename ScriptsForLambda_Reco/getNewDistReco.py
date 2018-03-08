import ROOT, sys, collections, math

# Set ATLAS style
def setATLASStyle(path="/afs/cern.ch/work/t/tvarol/bbyy_0917/scripts/createNewSampleDistr"):
    ROOT.gROOT.SetMacroPath(path)
    ROOT.gROOT.LoadMacro("AtlasStyle.C")
    ROOT.gROOT.LoadMacro("AtlasLabels.C")
    ROOT.gROOT.LoadMacro("AtlasUtils.C")
    ROOT.SetAtlasStyle() 

def compareHistograms(f0,f1,f2,histo="bb_pt",rebin=1):
    h0 = f0.Get(histo)
    h1 = f1.Get(histo)
    h2 = f2.Get(histo)
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
histList=['mass_bbyy_1t_l', 'mass_bbyy_1t_h', 'mass_bbyy_2t_l', 'mass_bbyy_2t_h', 'mass_jj_1t_l', 'mass_jj_1t_h', 'mass_jj_2t_l', 'mass_jj_2t_h', 'mass_yy_1t_l', 'mass_yy_1t_h','mass_yy_2t_l', 'mass_yy_2t_h']
xTitle=['m_{#gamma#gammabb} [GeV]', 'm_{#gamma#gammabb} [GeV]', 'm_{#gamma#gammabb} [GeV]', 'm_{#gamma#gammabb} [GeV]', 'm_{jj} [GeV]', 'm_{jj} [GeV]', 'm_{jj} [GeV]', 'm_{jj} [GeV]', 'm_{#gamma#gamma} [GeV]', 'm_{#gamma#gamma} [GeV]',  'm_{#gamma#gamma} [GeV]',  'm_{#gamma#gamma} [GeV]']
rebin=[2,2,2,2,5,5,5,5,1,1,1,1]

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
output = ROOT.TFile(outFileName, "RECREATE")

output.cd();
for idx,hist in enumerate(histList):
    hCalc = compareHistograms(f0,f1,f2,hist,rebin[idx])
    hCalc.Write()

output.Close()
