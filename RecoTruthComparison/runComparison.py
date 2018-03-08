import ROOT, sys, collections, math, csv, array

fW = open("yield_weighted.csv")
data_weighted = list(csv.reader(fW))

fR = open("yield_reco.csv")
data_reco = list(csv.reader(fR))

headerW = data_weighted[0]
data_weighted = data_weighted[1:]

headerR = data_reco[0]
data_reco = data_reco[1:]

oneTag = False

# Set ATLAS style                                                                                                                                          
def setATLASStyle(path="/afs/cern.ch/work/t/tvarol/bbyy_0917/scripts/createNewSampleDistr"):
    ROOT.gROOT.SetMacroPath(path)
    ROOT.gROOT.LoadMacro("AtlasStyle.C")
    ROOT.gROOT.LoadMacro("AtlasLabels.C")
    ROOT.gROOT.LoadMacro("AtlasUtils.C")
    ROOT.SetAtlasStyle()

# divide two histograms                                                                                                                                    
def divideHistogramsTH1F(h1,h2):
    h1clone=h1.Clone()
    h2clone=h2.Clone()
    h1clone.Divide(h1clone,h2clone)
    return h1clone

# divide two histograms by turning them into TGraph                                                                                                        
def divideHistograms(h1,h2):
    ratio_h1h2 = ROOT.myTGraphErrorsDivide(h1,h2)
    ratio_h1h2_result = ROOT.TGraphAsymmErrors()
    x1 = ROOT.Double(0.)
    y1 = ROOT.Double(0.)
    newIndex = 0
    for kk in xrange(ratio_h1h2.GetN()):
        ratio_h1h2.GetPoint(kk,x1,y1)
        if(math.fabs(y1)>0):
            ratio_h1h2_result.SetPoint(newIndex, x1, y1)
            ratio_h1h2_result.SetPointError(newIndex,
                                            0, #ratio_h1h2.GetErrorXlow(kk),                                                                          
                                            0, #ratio_h1h2.GetErrorXhigh(kk),                                                                            
                                            ratio_h1h2.GetErrorYlow(kk),
                                            ratio_h1h2.GetErrorYhigh(kk))
            newIndex = newIndex + 1
    return ratio_h1h2_result

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetErrorX(0)
setATLASStyle()

xW  = array.array('d')
yW  = array.array('d')
exW = array.array('d')
eyW = array.array('d')
nW = len(data_weighted)
print nW
for row in data_weighted:
  xW.append(float(row[0]))
  exW.append(0.)
  if oneTag:
      yW.append(float(row[1]))
      eyW.append(float(row[2]))
  else:
      yW.append(float(row[3]))
      eyW.append(float(row[4]))

grW = ROOT.TGraphErrors(nW, xW, yW, exW, eyW)

xR  = array.array('d')
yR  = array.array('d')
exR = array.array('d')
eyR = array.array('d')
nR = len(data_reco)
print nR
for row in data_reco:
  xR.append(float(row[0]))
  exR.append(0.)
  if oneTag:
      yR.append(float(row[1]))
      eyR.append(float(row[2]))
  else:
      yR.append(float(row[3]))
      eyR.append(float(row[4]))

grR = ROOT.TGraphErrors(nR, xR, yR, exR, eyR)

dummy = ROOT.TH1F("dummy","dummy", 60, -30., 30.)
dummy.GetYaxis().SetRangeUser(0,50.)

dummyHisto = ROOT.TH1F("dummyHisto","dummyHisto", 60, -30., 30.)
dummyHisto.GetYaxis().SetRangeUser(0.5,1.5)

# Draw canvas                                                                                                                                             
canvas = ROOT.TCanvas('c1','c1',800,800)
canvas.SetFillColor(0)

topPad = ROOT.TPad('pTop','pTop',0,0.2,1,1)
topPad.SetBottomMargin(0.13)
topPad.Draw()
botPad = ROOT.TPad('pBot','pBot',0,0.0,1,0.3)
botPad.Draw()
botPad.SetBottomMargin(0.30)

# Top Pad                                                                                                                                                   
topPad.cd()
grW.GetYaxis().SetTitle('Number of Expected Events [L=36^{-1}]')
grW.GetYaxis().SetTitleSize(0.05)
grW.GetYaxis().SetLabelSize(0.05)
grW.GetXaxis().SetLabelOffset(10)
grW.SetMarkerColor(1);
grW.SetLineColor(1);
grW.SetMarkerStyle(22);
grR.SetMarkerColor(2)
grR.SetLineColor(2);
grR.SetMarkerStyle(20)

dummy.Draw()
grW.Draw("Psame")
grR.Draw("Psame")

legend=ROOT.TLegend(0.7,0.75,0.9,0.9)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.AddEntry(grW,"Suggested",'lp')
legend.AddEntry(grR,"Current",'lp')
legend.Draw()
ROOT.gPad.RedrawAxis()

# Bottom Pad                                                                                                                                             
botPad.cd()
ratio = ROOT.myTGraphErrorsDivide(grW,grR)
#ratio = divideHistograms(grW,grR)
dummyHisto.GetXaxis().SetTitle('#lambda')
dummyHisto.GetXaxis().SetLabelSize(0.1)
dummyHisto.GetXaxis().SetLabelOffset(0.05)
dummyHisto.GetYaxis().SetLabelSize(0.12)
dummyHisto.GetYaxis().SetTitle('Suggested/Current')
dummyHisto.GetXaxis().SetTitleSize(0.1)
dummyHisto.GetYaxis().SetTitleSize(0.1)
dummyHisto.GetYaxis().SetTitleOffset(0.5)
dummyHisto.GetYaxis().SetNdivisions(5);
dummyHisto.Draw()
ratio.Draw("p&&0&&1&&same")
ROOT.gPad.SetGridx(1)
ROOT.gPad.SetGridy(1)

line = ROOT.TLine(dummyHisto.GetXaxis().GetXmin(),1,dummyHisto.GetXaxis().GetXmax(),1);
line.SetLineColor(2)
line.SetLineWidth(2)
line.Draw()
ratio.Draw("psame")
canvas.SaveAs('ratio.pdf')
