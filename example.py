import ROOT, tdrstyle, sys, os, array

low_pt=30
high_pt=200
endcap = -1
layer=1
x_var = "dphi" #"BA" or "rdphi" or "dphi"
cls = 6
gaus_low = -2
gaus_high = 2

f = ROOT.TFile("../Run2022DEFG_ZMu_PromptReco_RAWRECO_globalMu_pfisotight_aligned_v0.root")

event = f.Get("analyzer/ME11Seg_Prop")

if x_var == "BA":
  xlow = -10
  xhigh = 10
  x_plot = "1000*bending_angle"
  x_axis = "Bending Angle [mrad]"
elif x_var == "rdphi":
  xlow = -2
  xhigh = 2
  x_plot = "RdPhi_Corrected"
  x_axis = "#DeltaR#phi [cm]"
elif x_var == "dphi":
  xlow = -3
  xhigh = 3
  x_plot = "1000*dPhi_Corrected" #"-1000*(rechit_localphi_rad-prop_localphi_rad)"
  x_axis = "#Delta#phi [mRad]"

if endcap==1:
  reg_string="+"
elif endcap==-1:
  reg_string="-"

ROOT.gROOT.SetBatch(1)
tdrstyle.setTDRStyle()

H_ref = 800
W_ref = 800
W = W_ref
H = H_ref

T = 0.12*H_ref
B = 0.16*H_ref
L = 0.16*W_ref
R = 0.08*W_ref

xbins = 200
ybins = 100
xlow = xlow
xhigh = xhigh
ylow = -300
yhigh = 300
zlow = -2
zhigh = 2

canvas = ROOT.TCanvas("c1", "c1", 100, 100, W, H)
canvas.SetFillColor(0)
canvas.SetBorderMode(0)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.SetLeftMargin( L/W )
canvas.SetRightMargin( R/W )
canvas.SetTopMargin( T/H )
canvas.SetBottomMargin( B/H )
canvas.SetTickx(0)
canvas.SetTicky(0)
#canvas.SetLogy()
canvas.SetGrid()

h1 = ROOT.TH1D("h1", "h1", xbins, xlow, xhigh)
h2 = ROOT.TH1D("h2", "h2", xbins, xlow, xhigh)
h3 = ROOT.TH1D("h3", "h3", xbins, xlow, xhigh)
h4 = ROOT.TH1D("h4", "h4", xbins, xlow, xhigh)
h5 = ROOT.TH1D("h5", "h5", xbins, xlow, xhigh)
h6 = ROOT.TH1D("h6", "h6", xbins, xlow, xhigh)
h7 = ROOT.TH1D("h7", "h7", xbins, xlow, xhigh)
h8 = ROOT.TH1D("h8", "h8", xbins, xlow, xhigh)

cut = "(prop_location[2]==14 || prop_location[2]==16 || prop_location[2]==18 || prop_location[2]==20 || prop_location[2]==22 || prop_location[2]==24)"

#layer = prop_location[3]
#chamber = prop_location[2]
#region or endcap = prop_location[0]

h = [h1, h2, h3, h4, h5, h6, h7, h8]

for eta in [1,8]:#range(1, 9):
  event.Project("h{i}".format(i=eta), "{x}".format(x=x_plot), "muon_pt>{low} && muon_pt<{high} && n_ME11_segment==1 && has_fidcut && abs(RdPhi_Corrected) < 2 && prop_location[0]=={reg} && prop_location[3]=={lay} && prop_location[4]=={eta} && rechit_CLS=={cls} && has_TightID && {cut}".format(low=low_pt, high=high_pt, reg=endcap, lay=layer, cls=cls, eta=eta, cut=cut))

  h[eta-1].SetLineWidth(3) #3

  h[eta-1].SetMarkerSize(0)

  xAxis = h[eta-1].GetXaxis()
  xAxis.SetTitleOffset(1)
  xAxis.SetTitleSize(0.05)
  if x_var == "BA":
    xAxis.SetNdivisions(-505)
  xAxis.SetTitle("{x_axis}".format(x_axis=x_axis))

  yAxis = h[eta-1].GetYaxis()
  yAxis.SetTitleOffset(0)
  yAxis.SetTitleSize(0.05)
  yAxis.SetTitle("Entries")

  yAxis.SetRangeUser(0, 1.4*h[eta-1].GetMaximum())
  yAxis.SetMaxDigits(3)

  h[eta-1].Draw("HIST")

  f1 = ROOT.TF1("f1", "[0]* exp(-0.5*((x-[1])/[2])**2) + [3]* exp(-0.5*((x-[4])/[5])**2)", gaus_low, gaus_high)
  f1.SetParameters(.1,.1,.1,.1,.1,.1)
  f1.SetLineColor(ROOT.kRed)
  f1.SetMarkerSize(0)
  h[eta-1].Fit("f1")
  f1.Draw("same")


  legend = ROOT.TLegend(0.3, 0.7, 0.9, 0.85)
  legend.AddEntry(h[eta-1], "mean: {m}".format(m=round(h[eta-1].GetMean(), 3)))
  legend.AddEntry(h[eta-1], "RMS: {s}".format(s=round(h[eta-1].GetStdDev(), 3)))
  legend.AddEntry(f1, "mean: {m1}#pm{m1e}, {m2}#pm{m2e}".format(m1=round(f1.GetParameter(1), 3), m1e=round(f1.GetParError(1), 3), m2=round(f1.GetParameter(4), 3), m2e=round(f1.GetParError(4), 3)))
  legend.AddEntry(f1, "#sigma: {s1}#pm{s1e}, {s2}#pm{s2e}".format(s1=round(abs(f1.GetParameter(2)), 3), s1e=round(abs(f1.GetParError(2)), 3), s2=round(abs(f1.GetParameter(5)), 3), s2e=round(abs(f1.GetParError(5)), 3)))
  legend.SetTextSize(0.)
  legend.SetBorderSize(0)
  legend.Draw()

  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextAngle(0)
  latex.SetTextColor(ROOT.kBlack)

  latex.SetTextFont(42)
  latex.SetTextSize(0.3*canvas.GetTopMargin())

  latex.SetTextAlign(32)
  latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "(13.6 TeV)")
  latex.SetTextAlign(12)

  latex.DrawLatex(0.4+1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "2022DEFG")

  latex.SetTextSize(0.25*canvas.GetTopMargin())
  latex.DrawLatex(0.25-0.3*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.6*canvas.GetTopMargin(), "{reg}Endcap Chambers 14, 16, 18, 20, 22, 24 Layer {lay} CLS {cls}".format(reg=reg_string, lay=layer, cls=cls, eta=eta))
  latex.DrawLatex(0.25-0.3*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.9*canvas.GetTopMargin(), "#eta{eta}".format(eta=eta))

  latex.SetTextSize(0.5*canvas.GetTopMargin())
  latex.SetTextFont(61)
  latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-0.27*canvas.GetTopMargin(), "CMS")
  latex.SetTextFont(52)
  latex.SetTextSize(0.3*canvas.GetTopMargin())
  latex.DrawLatex(1.9*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "Preliminary")

  latex.SetTextFont(42)
  latex.SetTextSize(0.4*canvas.GetTopMargin())

###fit function part below
  latex.SetTextAlign(12)
  latex.SetTextSize(0.03)
  latex.SetTextFont(61)
  latex.DrawLatex(0.3*canvas.GetLeftMargin(), -0.04+ 0.5*canvas.GetBottomMargin(), "{zer}* exp(-0.5*((x- {one}) / {two})^2) + {three}* exp(-0.5*((x- {four}) / {five})^2)".format(zer = round(f1.GetParameter(0), 0), one = round(f1.GetParameter(1), 2), two = round(f1.GetParameter(2), 2), three = round(f1.GetParameter(3), 0), four = round(f1.GetParameter(4), 2), five = round(f1.GetParameter(5), 2) ))

###


  frame = canvas.GetFrame()
  frame.Draw()

  canvas.SaveAs("Run2022DEFG/ZMu_PromptReco_RAWRECO_globalMu_pfisotight_aligned_v0/tight/clusterSize{cls}_phi_1D_R{reg}L{lay}_Chamber{ch}_eta{eta}.png".format(reg=endcap, lay=layer, x_var=x_var, ch=1424, cls=cls, eta=eta))
