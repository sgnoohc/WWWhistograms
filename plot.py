import ROOT

from style import *

setStyle()


def draw_cms_lumi(c1, opts ):#, _persist=[]):

	c1.cd()
	t = ROOT.TLatex()
	t.SetTextAlign(11) # align bottom left corner of text
	t.SetTextColor(ROOT.kBlack)
	t.SetTextSize(0.04)
	# get top left corner of current pad, and nudge up the y coord a bit
	xcms  = ROOT.gPad.GetX1() + opts["canvas_main_leftmargin"]
	ycms  = ROOT.gPad.GetY2() - opts["canvas_main_topmargin"] + 0.035
	xlumi = ROOT.gPad.GetX2() - opts["canvas_main_rightmargin"]
	cms_label = opts["cms_label"]
	lumi_value = str(opts["lumi_value"])
	lumi_unit = opts["lumi_unit"]
	energy = 13
	if cms_label is not None:
	    t.DrawLatexNDC(xcms,ycms,"#scale[1.25]{#font[61]{CMS}} #scale[1.1]{#font[52]{%s}}" % cms_label)
	if lumi_value:
	    t.SetTextSize(0.04)
	    t.SetTextAlign(31) # align bottom right
	    t.SetTextFont(42) # align bottom right
	    t.DrawLatexNDC(xlumi,ycms,"{lumi_str} {lumi_unit}^{{-1}} ({energy} TeV)".format(energy=energy, lumi_str=lumi_value, lumi_unit=lumi_unit))
	#_persist.append(t)
	return

def makePlot1D( histname, data, sigs, signal_labels, bgs, legend_labels , options ): #, _persist = []):

	opts = Options(options, kind="1dratio")

	
	if opts["canvas_width"] and opts["canvas_height"]:
	    width = opts["canvas_width"]
	    height = opts["canvas_height"]
	    c1 = ROOT.TCanvas("c1", histname, width, height)
	else: 
		c1 = ROOT.TCanvas()
	#_persist.append(c1) # need this to avoid segfault with garbage collection

	do_ratio = opts["do_ratio"]
	if do_ratio:
		pad_main = ROOT.TPad("pad1","pad1",0.0,opts["canvas_main_y1"],1.0,1.0)
		if opts["canvas_main_topmargin"]: pad_main.SetTopMargin(opts["canvas_main_topmargin"])
		if opts["canvas_main_rightmargin"]: pad_main.SetRightMargin(opts["canvas_main_rightmargin"])
		if opts["canvas_main_bottommargin"]: pad_main.SetBottomMargin(opts["canvas_main_bottommargin"])
		if opts["canvas_main_leftmargin"]: pad_main.SetLeftMargin(opts["canvas_main_leftmargin"])
		if opts["canvas_tick_one_side"]: pad_main.SetTicks(0, 0)
		else : pad_main.SetTicks(1, 1)
		pad_ratio = ROOT.TPad("pad2","pad2",0.0, 0.00, 1.0, opts["canvas_ratio_y2"])
		if opts["canvas_ratio_topmargin"]: pad_ratio.SetTopMargin(opts["canvas_ratio_topmargin"])
		if opts["canvas_ratio_rightmargin"]: pad_ratio.SetRightMargin(opts["canvas_ratio_rightmargin"])
		if opts["canvas_ratio_bottommargin"]: pad_ratio.SetBottomMargin(opts["canvas_ratio_bottommargin"])
		if opts["canvas_ratio_leftmargin"]: pad_ratio.SetLeftMargin(opts["canvas_ratio_leftmargin"])
		if opts["canvas_tick_one_side"]: pad_ratio.SetTicks(0,0)
		else: pad_ratio.SetTicks(1,1)
		pad_main.Draw()
		pad_ratio.Draw()
	else:
	    pad_main = ROOT.TPad("pad1","pad1",0.,0.,1.,1.)
	    #if opts["canvas_main_topmargin"]: pad_main.SetTopMargin(opts["canvas_main_topmargin"])
	    #if opts["canvas_main_rightmargin"]: pad_main.SetRightMargin(opts["canvas_main_rightmargin"])
	    #if opts["canvas_main_bottommargin"]: pad_main.SetBottomMargin(opts["canvas_main_bottommargin"])
	    #if opts["canvas_main_leftmargin"]: pad_main.SetLeftMargin(opts["canvas_main_leftmargin"])
	    #if opts["canvas_tick_one_side"]: 
	    pad_main.SetTicks(0, 0)
	    pad_main.Draw()

	pad_main.cd()

	

	# 
	# stack
	# 
	stack = ROOT.THStack("stack", "")
	total = background_style(bgs[0].Clone("total"),opts)
	total.Reset()
	for ibg,bg in enumerate(bgs):
		#print (bg.GetName())
		background_style(bg,opts)
		total.Add(bg)
		stack.Add(bg)
		
		#legend.AddEntry(bg, legend_labels[ibg], "F")

	for isig,sig in reversed(list(enumerate(sigs))):
		if opts["stack_sig"]:
			signal_style(sig,opts)
			total.Add(sig)
			stack.Add(sig)
			
			#legend.AddEntry(sig, signal_labels[isig], "F")
	


	if opts["yaxis_range"]:
	    stack.SetMinimum(opts["yaxis_range"][0])
	    stack.SetMaximum(opts["yaxis_range"][1])
	    ymin, ymax = opts["yaxis_range"]
	else: 	
		ymin, ymax = 0., get_stack_maximum(data,stack,opts)
		ymax = 1.3*ymax if opts["do_stack"] else 1.00*ymax
	stack.SetMaximum(ymax)


	drawopt = "hist"
	stack.Draw(drawopt)
	stack.GetHistogram().GetXaxis().SetLabelSize(0)
	stack.GetHistogram().GetXaxis().SetTitleSize(0)
	if opts["xaxis_range"] : stack.GetXaxis().SetRangeUser( *opts["xaxis_range"])	

	if opts["yaxis_label"]: stack.GetHistogram().GetYaxis().SetTitle(opts["yaxis_label"])
	if opts["yaxis_title_size"]: stack.GetHistogram().GetYaxis().SetTitleSize(opts["yaxis_title_size"])
	if opts["yaxis_title_offset"] : stack.GetHistogram().GetYaxis().SetTitleOffset(opts["yaxis_title_offset"]) 

	#
	# stat errors - from total  
	#
	#if not opts["no_overflow"]: utils.move_in_overflows(bgs_syst)
	total.SetMarkerSize(0)
	total.SetLineWidth(0)
	total.SetFillColor(ROOT.kBlack)
	total.SetFillStyle(opts["bkg_err_fill_style"])
	total.Draw("E2 SAME")


	ratio_err = total.Clone("ratio_err")
	#ratio_err.Sumw2()
	ratio_err.Divide(total)
	ratio_err.SetFillColor(ROOT.kBlack)
	#ratio_err.SetFillColorAlpha(ROOT.kGray+2,0.4)
	ratio_err.SetFillStyle(opts["ratio_err_fill_style"])

	
	# 
	# Signal if not stack
	# 
	if not opts["stack_sig"]:
		for sig in enumerate(sigs): 
			signal_style(sig,opts)
			sig.Draw("samehist")

	#
	# data 
	#
	data_style(data,opts)
	#legend.AddEntry(data,"Data","LPE")
	data.Draw("same pe X0")

	# misc
	draw_cms_lumi(c1, opts)
	pad_main.cd()

	# legend, some unfortunate hardcoding
	opts["legend_ncolumns"]  = 1 #if len(bgs) >= 4 else 1
	opts["legend_alignment"] = "topleft"
	opts["legend_smart"]    = True
	opts["legend_scalex"]   = 0.5
	opts["legend_scaley"]   = 0.9
	opts["legend_border"]   = False
	opts["legend_rounded"]  = False
	legend = get_legend(opts)
	sig_opt = "F"
	legend.AddEntry(sigs[0],signal_labels[0],sig_opt) #1
	legend.AddEntry(sigs[1],signal_labels[1],sig_opt) #2
	legend.AddEntry(sigs[2],signal_labels[2],sig_opt) #3
	legend.AddEntry(sigs[3],signal_labels[3],sig_opt) #4
	legend.Draw()

	# data leg
	opts["legend_ncolumns"]  = 1 #if len(bgs) >= 4 else 1
	opts["legend_alignment"] = "topmiddle"
	opts["legend_smart"]    = True
	opts["legend_scalex"]   = 0.8
	opts["legend_scaley"]   = 0.45
	legend2 = get_legend(opts)
	legend2.AddEntry(data,"Data","pl") #1
	legend2.AddEntry(total,"Stat. Uncert.","f") #2
	legend2.Draw()

	# bkg leg, some unfortunate hardcoding
	opts["legend_ncolumns"]  = 2 #if len(bgs) >= 4 else 1
	opts["legend_alignment"] = "topright"
	opts["legend_smart"]    = True
	opts["legend_scalex"]   = 1.4
	opts["legend_scaley"]   = 0.8
	bkg_opt = "F"
	legend3 = get_legend(opts)
	legend3.AddEntry(bgs[3],legend_labels[3],bkg_opt) #1, gamma
	legend3.AddEntry(bgs[0],legend_labels[0],bkg_opt) #2
	legend3.AddEntry(bgs[1],legend_labels[1],bkg_opt) #1, gamma
	legend3.AddEntry(bgs[4],legend_labels[4],bkg_opt) #2
	legend3.AddEntry(bgs[2],legend_labels[2],bkg_opt) #2
	legend3.Draw()

	
	        
	# ratio 
	if opts["do_ratio"]:

		pad_ratio.cd()

		# compute reatio 
		numer = data.Clone("numer")
		denom = total.Clone("sumbgs")
		ratio = numer.Clone("ratio")
		if opts["ratio_binomial_errors"]:
		    ratio.Divide(numer,denom,1,1,"b")
		else:
		    ratio.Divide(denom)

		ratio.Draw("axis")
		ratio_err.Draw("E2 SAME")
		do_style_ratio(ratio, opts, pad_ratio)
		ratio.Draw("same PE X0")

		line = ROOT.TLine()
		line.SetLineColor(ROOT.kGray+2)
		line.SetLineWidth(1)
		for yval in opts["ratio_horizontal_lines"]:
		    
		    if opts["xaxis_range"]: line.DrawLine(opts["xaxis_range"][0],yval,opts["xaxis_range"][1],yval)
		    else: line.DrawLine(ratio.GetXaxis().GetBinLowEdge(1),yval,ratio.GetXaxis().GetBinUpEdge(ratio.GetNbinsX()),yval)

		pad_main.cd()

	

	save(c1, opts)
	return


def makePlot(sr, name , dirname, extraoptions={}):

	histname = "{}__{}".format(sr,name)

	input_dir = "hists/combineyearsLoose_v5.3.3/2020_03_09_1500"
	
	data_fname = "{}/data.root".format(input_dir)
	
	bkg_fnames = [
	    "{}/photon.root".format(input_dir),
	    "{}/qflip.root".format(input_dir),
	    "{}/fakes.root".format(input_dir), # may want to take fakes from data
	    "{}/lostlep.root".format(input_dir),
	    "{}/prompt.root".format(input_dir),
	    ]

	# background file names
	sig_fnames = [
	    "{}/www.root".format(input_dir),
	    "{}/wwz.root".format(input_dir),
	    "{}/wzz.root".format(input_dir), 
	    "{}/zzz.root".format(input_dir),
		]

	# get histos
	data = getHisto(data_fname,histname)
	bgs  = getHistos(bkg_fnames,histname)
	sigs = getHistos(sig_fnames,histname)

	legend_labels = [
		"#gamma#rightarrowl",
		"Charge mis-id",
		"Non-prompt leptons",
		"Lost lep/three leptons",
		"Irreducible"
		]
	signal_labels = [
		"WWW",
		"WWZ",
		"WZZ",
		"ZZZ"
		]

	options = {
		"output_name": dirname + "/" + histname + ".png",
		"do_ratio": True,
		"stack_sig": True,
		}
	options.update(extraoptions)

	makePlot1D( histname, data, sigs, signal_labels, bgs, legend_labels, options )

	return 

def makePlotMultipleSRs(srs, selname, name , dirname, extraoptions={}):


	input_dir = "hists/combineyearsLoose_v5.3.3/2020_03_09_1500"
	
	data_fname = "{}/data.root".format(input_dir)
	
	bkg_fnames = [
	    "{}/photon.root".format(input_dir),
	    "{}/qflip.root".format(input_dir),
	    "{}/fakes.root".format(input_dir), # may want to take fakes from data
	    "{}/lostlep.root".format(input_dir),
	    "{}/prompt.root".format(input_dir),
	    ]

	# background file names
	sig_fnames = [
	    "{}/www.root".format(input_dir),
	    "{}/wwz.root".format(input_dir),
	    "{}/wzz.root".format(input_dir), 
	    "{}/zzz.root".format(input_dir),
		]

	# get histos
	data  = getMultipleSRHisto(data_fname ,srs,selname,name)
	bgs   = getMultipleSRHistos(bkg_fnames,srs,selname,name)
	sigs  = getMultipleSRHistos(sig_fnames,srs,selname,name)
 

	legend_labels = [
		"#gamma#rightarrowl",
		"Charge mis-id",
		"Non-prompt leptons",
		"Lost lep/three leptons",
		"Irreducible"
		]
	signal_labels = [
		"WWW",
		"WWZ",
		"WZZ",
		"ZZZ"
		]

	histname = "{}__{}".format(selname,name)
	options = {
		"output_name": dirname + "/" + histname + ".png",
		"do_ratio": True,
		"stack_sig": True,
		}
	options.update(extraoptions)

	histname = "{}__{}".format(selname,name)
	makePlot1D( histname, data, sigs, signal_labels, bgs, legend_labels, options )

	return 



def makeSS2Jplots(dirname):
	#
	# 2j SS Kin selection 
	#
	srs = ["SRSSeeKinSel","SRSSemKinSel","SRSSmmKinSel"]
	
	# Mjj
	options = {
	 "yaxis_label": "Events",
	 "xaxis_label": "M_{jj} [GeV]",
	 "nbins": 20,
	}
	makePlotMultipleSRs(srs, "SRSS2jKinSel", "Mjj" , dirname, options)
	
	#
	# 2j SS Preselection 
	#
	srs = ["SRSSeePreSel","SRSSemPreSel","SRSSmmPreSel"]
	
	# MET 
	options = {
	 "yaxis_label": "Events",
	 "xaxis_label": "M_{jj} [GeV]",
	 "nbins": 20,
	}
	makePlotMultipleSRs(srs, "SRSSPreSel", "Mjj" , dirname, options)
	
	#MTmax 
	options = {
	 "yaxis_label": "Events",
	 "xaxis_label": "M_{T}^{max} [GeV]",
	 "nbins": 20,
	}
	makePlotMultipleSRs(srs, "SRSSPreSel", "MTmax" , dirname, options)
	return

def makeSS1Jplots(dirname):
	#
	# 1j - SS Preselection
	# 
	srs = ["SRSS1Jee1JPre","SRSS1Jem1JPre","SRSS1Jmm1JPre"]
	sel = "SRSS1JPreSel"
	
	# MET 
	options = {
	 "yaxis_label": "Events",
	 "xaxis_label": "E_{T}^{miss} [GeV]",
	 "nbins": 15,
	}
	makePlotMultipleSRs(srs, sel, "MET" , dirname, options)
	
	# DRljmin 
	options = {
	 "yaxis_label": "Events",
	 "xaxis_label": "#DeltaR^{min}(l,j) [GeV]",
	 "nbins": 15,
	}
	makePlotMultipleSRs(srs, sel, "DRljmin" , dirname, options)
	
	# MTmax 
	options = {
	 "yaxis_label": "Events",
	 "xaxis_label": "M_{T}^{max} [GeV]",
	 "nbins": 15,
	}
	makePlotMultipleSRs(srs, sel, "MTmax" , dirname, options)

	return

def make0SFOSplots(dirname):
	#
	# 3l - preselelctin
	#
	srs = ["SR0SFOSeemPreSel","SR0SFOSemmPreSel"]
	sel = "SR0SFOSPreSel"

	# trying looser than presel
	srs = ["SR0SFOSeem","SR0SFOSemm"]
	sel = "SR0SFOS"

	# MTmax 
	options = {
	 "yaxis_label": "Events",
	 "yaxis_range": [0,25],
	 "xaxis_label": "M_{T}^{max} [GeV]",
	 "nbins": 15,
	}
	makePlotMultipleSRs(srs, sel, "MTmax" , dirname, options)

	# pT3l
	options = {
	 "yaxis_label": "Events",
	 "yaxis_range": [0,40],
	 "xaxis_label": "p_{T}^{max}(3l) [GeV]",
	 "nbins": 15,
	}
	makePlotMultipleSRs(srs, sel, "Pt3l" , dirname, options)

	# dR3lmet
	options = {
	 "yaxis_label": "Events",
	 "yaxis_range": [0,30],
	 "xaxis_label": "#Delta#phi(3l,E_{T}^{miss}) [GeV]",
	 "nbins": 15,
	}
	makePlotMultipleSRs(srs, sel, "DPhi3lMET" , dirname, options)

	return 

def makeWZCRSSplots(dirname):
	#
	# 3l - preselelctin
	#
	srs = ["WZCRSSeePreSel","WZCRSSemPreSel","WZCRSSmmPreSel"]
	sel = "WZCRSSPreSel"

	# trying looser than presel
	#srs = ["SR0SFOSeem","SR0SFOSemm"]
	#sel = "SR0SFOS"

	# MTmax 
	options = {
	 "yaxis_label": "Events",
	 #"yaxis_range": [0,25],
	 "xaxis_label": "M_{jj} [GeV]",
	 "nbins": 20,
	}
	makePlotMultipleSRs(srs, sel, "Mjj" , dirname, options)

	# mT third
	options = {
	 "yaxis_label": "Events",
	 #"yaxis_range": [0,25],
	 "xaxis_label": "M_{T}^{3rd} [GeV]",
	 "nbins": 20,
	}
	makePlotMultipleSRs(srs, sel, "MT3rd" , dirname, options)

	# mT max
	options = {
	 "yaxis_label": "Events",
	 #"yaxis_range": [0,25],
	 "xaxis_label": "M_{T}^{max} [GeV]",
	 "nbins": 20,
	}
	makePlotMultipleSRs(srs, sel, "MTmax" , dirname, options)

	# SFOS
	options = {
	 "yaxis_label": "Events",
	 #"yaxis_range": [0,25],
	 "xaxis_label": "M_{ll}^{SFOS} [GeV]",
	 "xaxis_range": [70,110],
	 "nbins": 50,
	}
	makePlotMultipleSRs(srs, sel, "MllOnOff" , dirname, options)

	return 

def makeFakeCRplots(dirname):
	#
	# 3l - preselelctin
	#
	srs = ["CRBTageePreSel","CRBTagmmPreSel","CRBTagmmPreSel"]
	sel = "CRBTagPreSel"

	srs = ["CRBTag0SFOS"]
	sel = "CRBTag0SFOS"
	# trying tighter
	#srs = ["CRBTageeKinSel","CRBTagmmKinSel","CRBTagmmKinSel"]
	#sel = "CRBTagKinSel"
	# trying looser than presel
	#srs = ["SR0SFOSeem","SR0SFOSemm"]
	#sel = "SR0SFOS"

	# lead lep pT 
	options = {
	 "yaxis_label": "Events",
	 "yaxis_range": [0,50],
	 "xaxis_label": "Leading lepton p_{T} [GeV]",
	 "nbins": 10,
	}
	makePlotMultipleSRs(srs, sel, "lep_pt0" , dirname, options)

	# MT
	options = {
	 "yaxis_label": "Events",
	 "yaxis_range": [0,35],
	 "xaxis_label": "M_{T}^{max} [GeV]",
	 "nbins": 10,
	}
	makePlotMultipleSRs(srs, sel, "MTmax" , dirname, options)

	return 

# Plot things...
dirname = "plots"
#makeSS2Jplots(dirname)
#makeSS1Jplots(dirname)
#make0SFOSplots(dirname)
#
#makeWZCRSSplots(dirname)
makeFakeCRplots(dirname)

# test SS njets 
srs = ["SRSSee","SRSSem","SRSSmm"]
sel = "SRSS"

options = {
 "yaxis_label": "Events",
 "xaxis_label": "N_{jets}",
}
makePlotMultipleSRs(srs, sel, "nj" , dirname, options)

options = {
 "yaxis_label": "Events",
 "xaxis_label": "N_{b-jets}",
}
makePlotMultipleSRs(srs, sel, "nb" , dirname, options)

# test 


