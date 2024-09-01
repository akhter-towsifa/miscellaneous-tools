import ROOT, tdrstyle, sys, os, array

low_pt=5
high_pt=200
endcap=-1
layer=1

f = ROOT.TFile("path_to_your_file.root")
event = f.Get("analyzer/ME11Seg_Prop")

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

xbins = 100
ybins = 100
xlow = -2
xhigh = 2
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
canvas.SetGrid()
#canvas.SetLogy()

h0 = ROOT.TH1D("h0", "h0", xbins, xlow, xhigh)

xAxis = h0.GetXaxis()
xAxis.SetTitleOffset(1)
xAxis.SetTitleSize(0.05)
xAxis.SetTitle("#DeltaR#phi [cm]")

yAxis = h0.GetYaxis()
yAxis.SetTitleOffset(0)
yAxis.SetTitleSize(0.05)
yAxis.SetTitle("A.U.")

#layer = prop_location[3]
#chamber = prop_location[2]
#region or endcap = prop_location[0]

event.Project("h0", "RdPhi_Corrected", "muon_pt>{low} && muon_pt<{high} && n_ME11_segment==1 && has_fidcut && abs(RdPhi_Corrected) < 2 && prop_location[0]=={reg} && prop_location[3]=={lay}".format(low=low_pt, high=10, reg=endcap, lay=layer))

h0.Scale(1/h0.Integral())
h0.SetLineWidth(3)
h0.SetMarkerSize(0)
h0.Draw("HIST")

#f1 = ROOT.TF1("f1", "[0]* exp([1]*x**2 + [2]) + [3]* exp([4]*x**2 + [5])", -1.5, 1.5)
#f1 = ROOT.TF1("f1", "[0]* exp(-0.5*((x-[1])/[2])**2) + [3]* exp(-0.5*((x-[4])/[5])**2)", gaus_low, gaus_high)
#f1 = ROOT.TF1("f1", "gaus(0)+gaus(3)", gaus_low, gaus_high)
#f1.SetParameters(h.GetMaximum(), h.GetMean(), h.GetStdDev(), h.GetMaximum(), h.GetMean(), h.GetStdDev())
#f1.SetParameters(.1,.1,.1,.1,.1,.1)
#f1.SetLineColor(ROOT.kRed)
#f1.SetMarkerSize(0)
#h.Fit("f1")
#f1.Draw("same")

latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextAngle(0)
latex.SetTextColor(ROOT.kBlack)

latex.SetTextFont(42)
latex.SetTextSize(0.3*canvas.GetTopMargin())

latex.SetTextAlign(32)
latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.3*canvas.GetTopMargin(), "Entries: {entries}".format(entries = int(h0.GetEntries())))
latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.7*canvas.GetTopMargin(), "Mean: {mean}".format(mean = round(h0.GetMean(),3)))
latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.1*canvas.GetTopMargin(), "Std Dev: {stddev}".format(stddev = round(h0.GetStdDev(),3)))
latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "(13.6 TeV)")
latex.SetTextAlign(12)

latex.SetTextSize(0.25*canvas.GetTopMargin())
latex.DrawLatex(0.65-0.3*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-2.0*canvas.GetTopMargin(), "{reg}Endcap Layer {lay}".format(reg=reg_string, lay=layer))

latex.SetTextSize(0.5*canvas.GetTopMargin())
latex.SetTextFont(61)
latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-0.27*canvas.GetTopMargin(), "CMS")
latex.SetTextFont(52)
latex.SetTextSize(0.3*canvas.GetTopMargin())
latex.DrawLatex(1.9*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "Preliminary")

latex.SetTextFont(42)
latex.SetTextSize(0.4*canvas.GetTopMargin())

frame = canvas.GetFrame()
frame.Draw()

canvas.SaveAs("R{reg}L{lay}.png".format(reg=endcap, lay=layer))
