import ROOT, sys, collections, math

# Set ATLAS style                                                                                                                               
def setATLASStyle(path="/afs/cern.ch/work/t/tvarol/bbyy_0917/scripts/createNewSampleDistr"):
    ROOT.gROOT.SetMacroPath(path)
    ROOT.gROOT.LoadMacro("AtlasStyle.C")
    ROOT.gROOT.LoadMacro("AtlasLabels.C")
    ROOT.gROOT.LoadMacro("AtlasUtils.C")
    ROOT.SetAtlasStyle()

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetErrorX(0)
setATLASStyle()

fW   = ROOT.TFile.Open("allWeights.root")

suffix=["25m","20m","15m","10m","9m","8m","7m","6m","5m","4m","2m","1m","0","1p","2p","3p","4p","5p","6p","7p","8p","9p","10p","15p","20p","25p"]

f = ROOT.TFile.Open("tree-NLO.root")
output = ROOT.TFile("weightedNLO.root", "RECREATE")
output.cd();

histList=collections.OrderedDict()

for sample in suffix:

    hist_m_yy_1t_l = ROOT.TH1F("mass_yy_1t_l_"+sample,"mass_yy_1t_l_"+sample, 50, 100., 150.)
    hist_m_yy_1t_h = ROOT.TH1F("mass_yy_1t_h_"+sample,"mass_yy_1t_h_"+sample, 50, 100., 150.)
    hist_m_yy_2t_l = ROOT.TH1F("mass_yy_2t_l_"+sample,"mass_yy_2t_l_"+sample, 50, 100., 150.)
    hist_m_yy_2t_h = ROOT.TH1F("mass_yy_2t_h_"+sample,"mass_yy_2t_h_"+sample, 50, 100., 150.)
    
    hist_m_bbyy_1t_l = ROOT.TH1F("mass_bbyy_1t_l_"+sample,"mass_bbyy_1t_l_"+sample, 130, 200., 1500.)
    hist_m_bbyy_1t_h = ROOT.TH1F("mass_bbyy_1t_h_"+sample,"mass_bbyy_1t_h_"+sample, 130, 200., 1500.)
    hist_m_bbyy_2t_l = ROOT.TH1F("mass_bbyy_2t_l_"+sample,"mass_bbyy_2t_l_"+sample, 130, 200., 1500.)
    hist_m_bbyy_2t_h = ROOT.TH1F("mass_bbyy_2t_h_"+sample,"mass_bbyy_2t_h_"+sample, 130, 200., 1500.)

    w_myybb = fW.Get("m_yybb_"+sample)

    for event in f.massDistr:
        weightForReco_myybb = w_myybb.GetBinContent(w_myybb.FindBin(event.m_bbyy_truth))
        
        if event.m_bbyy_1t_l >= 0: 
            hist_m_bbyy_1t_l.Fill(event.m_bbyy_1t_l, event.weight_l*weightForReco_myybb)           
        if event.m_bbyy_1t_h >= 0:
           hist_m_bbyy_1t_h.Fill(event.m_bbyy_1t_h, event.weight_h*weightForReco_myybb)
        if event.m_bbyy_2t_l >= 0:
            hist_m_bbyy_2t_l.Fill(event.m_bbyy_2t_l, event.weight_l*weightForReco_myybb)
        if event.m_bbyy_2t_h >= 0:
            hist_m_bbyy_2t_h.Fill(event.m_bbyy_2t_h, event.weight_h*weightForReco_myybb) 

    hist_m_bbyy_1t_l.Write()
    hist_m_bbyy_1t_h.Write()
    hist_m_bbyy_2t_l.Write()
    hist_m_bbyy_2t_h.Write()

    hist_m_bbyy_1t_l.Delete()
    hist_m_bbyy_1t_h.Delete()
    hist_m_bbyy_2t_l.Delete()
    hist_m_bbyy_2t_h.Delete()

output.Close()
fW.Close()

