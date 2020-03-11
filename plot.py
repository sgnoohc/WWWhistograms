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

def makePlot1DSafe( histname, data, sigs, signal_labels, bgs, legend_labels , options ): #, _persist = []):

	opts = Options(options, kind="1dratio")

	
	if opts["canvas_width"] and opts["canvas_height"]:
	    width = opts["canvas_width"]
	    height = opts["canvas_height"]
	    c1 = ROOT.TCanvas(histname, "", width, height)
	else: 
		c1 = ROOT.TCanvas(histname,"")
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
	#for ibg,bg in enumerate(bgs):
	for ibg,bg in reversed(list(enumerate(bgs))):
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
		ymax = 1.5*ymax if opts["do_stack"] else 1.00*ymax
		if opts["yaxis_log"] : 
			ymax = 10*ymax 
			ymin = 0.1

	stack.SetMaximum(ymax)


	drawopt = "hist"
	stack.Draw(drawopt)
	stack.GetHistogram().GetXaxis().SetLabelSize(0)
	stack.GetHistogram().GetXaxis().SetTitleSize(0)
	if opts["xaxis_range"] : stack.GetXaxis().SetRangeUser( *opts["xaxis_range"])	
	if opts["xaxis_ndivisions"] : stack.GetXaxis().SetNdivisions( opts["xaxis_ndivisions"])

	if opts["yaxis_label"]: stack.GetHistogram().GetYaxis().SetTitle(opts["yaxis_label"])
	if opts["yaxis_label_size"]: stack.GetHistogram().GetYaxis().SetLabelSize(opts["yaxis_label_size"])
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
	draw_extra_stuff(c1, opts)
	pad_main.cd()

	# legend, some unfortunate hardcoding
	opts["legend_ncolumns"]  = 1 #if len(bgs) >= 4 else 1
	opts["legend_alignment"] = "topleft"
	opts["legend_smart"]    = True
	opts["legend_scalex"]   = 0.5
	opts["legend_scaley"]   = 0.9
	opts["legend_border"]   = False
	opts["legend_rounded"]  = False
	#legend = get_legend(opts)
	#sig_opt = "F"
	#legend.AddEntry(sigs[0],signal_labels[0],sig_opt) #1
	#legend.AddEntry(sigs[1],signal_labels[1],sig_opt) #2
	#legend.AddEntry(sigs[2],signal_labels[2],sig_opt) #3
	#legend.AddEntry(sigs[3],signal_labels[3],sig_opt) #4
	#legend.Draw()

	# data leg
	#opts["legend_ncolumns"]  = 1 #if len(bgs) >= 4 else 1
	#opts["legend_alignment"] = "topleft"
	#opts["legend_smart"]    = True
	#opts["legend_scalex"]   = 0.8
	#opts["legend_scaley"]   = 0.45
	#legend2 = get_legend(opts)
	#legend2.Draw()

	# bkg leg, some unfortunate hardcoding
	opts["legend_ncolumns"]  = 4 #if len(bgs) >= 4 else 1
	opts["legend_alignment"] = "topright"
	opts["legend_smart"]    = True
	opts["legend_scalex"]   = 2.5
	opts["legend_scaley"]   = 0.6
	bkg_opt = "F"
	legend3 = get_legend(opts)
	legend3.AddEntry(data,"Data","pl") #0 
	legend3.AddEntry(sigs[0],signal_labels[0],bkg_opt) #1 
	legend3.AddEntry(bgs[0],legend_labels[0],bkg_opt) #3
	legend3.AddEntry(bgs[1],legend_labels[1],bkg_opt) #1
	legend3.AddEntry(total,"Stat. Uncert.","f") #0
	legend3.AddEntry(bgs[4],legend_labels[4],bkg_opt) #1
	legend3.AddEntry(bgs[2],legend_labels[2],bkg_opt) #2
	legend3.AddEntry(bgs[3],legend_labels[3],bkg_opt) #3
	#
	#legend3.AddEntry(data,"Data","pl") #0 
	#legend3.AddEntry(sigs[0],signal_labels[0],bkg_opt) #1 
	#legend3.AddEntry(bgs[4],legend_labels[4],bkg_opt) #2
	#legend3.AddEntry(bgs[3],legend_labels[3],bkg_opt) #3
	#legend3.AddEntry(total,"Stat. Uncert.","f") #0
	#legend3.AddEntry(bgs[0],legend_labels[0],bkg_opt) #1
	#legend3.AddEntry(bgs[1],legend_labels[1],bkg_opt) #2
	#legend3.AddEntry(bgs[2],legend_labels[2],bkg_opt) #3
	legend3.Draw()

	if opts["yaxis_log"] : pad_main.SetLogy(opts["yaxis_log"] )
	        
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

def makePlot1D( histname, data, sigs, signal_labels, bgs, legend_labels , options ): #, _persist = []):

	opts = Options(options, kind="1dratio")

	
	if opts["canvas_width"] and opts["canvas_height"]:
	    width = opts["canvas_width"]
	    height = opts["canvas_height"]
	    c1 = ROOT.TCanvas(histname, "", width, height)
	else: 
		c1 = ROOT.TCanvas(histname,"")
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
	#for ibg,bg in enumerate(bgs):
	for ibg,bg in reversed(list(enumerate(bgs))):
		#print (bg.GetName())
		background_style(bg,opts)
		total.Add(bg)
		stack.Add(bg)
		
		#legend.AddEntry(bg, legend_labels[ibg], "F")

	for isig,sig in reversed(list(enumerate(sigs))):
		if opts["stack_sig"]:
			signal_style(sig,opts)
			#total.Add(sig)
			stack.Add(sig)
			
			#legend.AddEntry(sig, signal_labels[isig], "F")
	
	if opts["yaxis_range"]:
	    stack.SetMinimum(opts["yaxis_range"][0])
	    stack.SetMaximum(opts["yaxis_range"][1])
	    ymin, ymax = opts["yaxis_range"]
	else: 	
		ymin, ymax = 0., get_stack_maximum(data,stack,opts)
		ymax = 1.5*ymax if opts["do_stack"] else 1.00*ymax
		if opts["yaxis_log"] : 
			ymax = 10*ymax 
			ymin = 0.1

	stack.SetMaximum(ymax)


	drawopt = "hist"
	stack.Draw(drawopt)
	stack.GetHistogram().GetXaxis().SetLabelSize(0)
	stack.GetHistogram().GetXaxis().SetTitleSize(0)
	if opts["xaxis_range"] : stack.GetXaxis().SetRangeUser( *opts["xaxis_range"])	
	if opts["xaxis_ndivisions"] : stack.GetXaxis().SetNdivisions( opts["xaxis_ndivisions"])

	if opts["yaxis_label"]: stack.GetHistogram().GetYaxis().SetTitle(opts["yaxis_label"])
	if opts["yaxis_label_size"]: stack.GetHistogram().GetYaxis().SetLabelSize(opts["yaxis_label_size"])
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
	ratio_err.Add(total,-1)
	#ratio_err.Divide(total)
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
	draw_extra_stuff(c1, opts)
	pad_main.cd()

	# legend, some unfortunate hardcoding
	opts["legend_ncolumns"]  = 1 #if len(bgs) >= 4 else 1
	opts["legend_alignment"] = "topleft"
	opts["legend_smart"]    = True
	opts["legend_scalex"]   = 0.5
	opts["legend_scaley"]   = 0.9
	opts["legend_border"]   = False
	opts["legend_rounded"]  = False
	#legend = get_legend(opts)
	#sig_opt = "F"
	#legend.AddEntry(sigs[0],signal_labels[0],sig_opt) #1
	#legend.AddEntry(sigs[1],signal_labels[1],sig_opt) #2
	#legend.AddEntry(sigs[2],signal_labels[2],sig_opt) #3
	#legend.AddEntry(sigs[3],signal_labels[3],sig_opt) #4
	#legend.Draw()

	# data leg
	#opts["legend_ncolumns"]  = 1 #if len(bgs) >= 4 else 1
	#opts["legend_alignment"] = "topleft"
	#opts["legend_smart"]    = True
	#opts["legend_scalex"]   = 0.8
	#opts["legend_scaley"]   = 0.45
	#legend2 = get_legend(opts)
	#legend2.Draw()

	# bkg leg, some unfortunate hardcoding
	opts["legend_ncolumns"]  = 4 #if len(bgs) >= 4 else 1
	opts["legend_alignment"] = "topright"
	opts["legend_smart"]    = True
	opts["legend_scalex"]   = 2.5
	opts["legend_scaley"]   = 0.6
	bkg_opt = "F"
	legend3 = get_legend(opts)
	legend3.AddEntry(data,"Data","pl") #0 
	legend3.AddEntry(sigs[0],signal_labels[0],bkg_opt) #1 
	legend3.AddEntry(bgs[0],legend_labels[0],bkg_opt) #3
	legend3.AddEntry(bgs[1],legend_labels[1],bkg_opt) #1
	legend3.AddEntry(total,"Stat. Uncert.","f") #0
	legend3.AddEntry(bgs[4],legend_labels[4],bkg_opt) #1
	legend3.AddEntry(bgs[2],legend_labels[2],bkg_opt) #2
	legend3.AddEntry(bgs[3],legend_labels[3],bkg_opt) #3
	#
	#legend3.AddEntry(data,"Data","pl") #0 
	#legend3.AddEntry(sigs[0],signal_labels[0],bkg_opt) #1 
	#legend3.AddEntry(bgs[4],legend_labels[4],bkg_opt) #2
	#legend3.AddEntry(bgs[3],legend_labels[3],bkg_opt) #3
	#legend3.AddEntry(total,"Stat. Uncert.","f") #0
	#legend3.AddEntry(bgs[0],legend_labels[0],bkg_opt) #1
	#legend3.AddEntry(bgs[1],legend_labels[1],bkg_opt) #2
	#legend3.AddEntry(bgs[2],legend_labels[2],bkg_opt) #3
	legend3.Draw()

	if opts["yaxis_log"] : pad_main.SetLogy(opts["yaxis_log"] )
	        
	# ratio 
	if opts["do_ratio"]:

		pad_ratio.cd()

		# compute reatio 
		numer = data.Clone("numer")
		denom = total.Clone("sumbgs")
		ratio = numer.Clone("ratio")
		ratio.Add(denom,-1)

		#if opts["ratio_binomial_errors"]:
		#    ratio.Divide(numer,denom,1,1,"b")
		#else:
		#    ratio.Divide(denom)

		
		ratio.Draw("axis")
		sigs[0].Draw("hist same")
		ratio_err.Draw("E2 SAME")
		ymax = max(ratio.GetMaximum(),sigs[0].GetMaximum())*1.1
		ymin = -ymax*0.5
		do_style_ratio(ratio, opts, pad_ratio)
		ratio.GetYaxis().SetRangeUser(ymin,ymax)
		ratio.GetYaxis().SetTitle("Data-Bkg.")

		ratio.Draw("same PE X0")

		line = ROOT.TLine()
		line.SetLineColor(ROOT.kGray+2)
		line.SetLineWidth(1)
		#for yval in opts["ratio_horizontal_lines"]:
		yval = 0
		if opts["xaxis_range"]: line.DrawLine(opts["xaxis_range"][0],yval,opts["xaxis_range"][1],yval)
		else: line.DrawLine(ratio.GetXaxis().GetBinLowEdge(1),yval,ratio.GetXaxis().GetBinUpEdge(ratio.GetNbinsX()),yval)
		#line.DrawLine(ratio.GetXaxis().GetBinLowEdge(1),yval,ratio.GetXaxis().GetBinUpEdge(ratio.GetNbinsX()),yval)

		pad_main.cd()

	

	save(c1, opts)
	return



def makePlotMultipleSRs(srs, selname, name , dirname, extraoptions={}):


	input_dir = "hists/combineyearsLoose_v5.3.3/2020_03_09_1500"
	
	data_fname = "{}/data.root".format(input_dir)
	
	bkg_fnames = [
		"{}/lostlep.root".format(input_dir),
		"{}/fakes.root".format(input_dir), # may want to take fakes from data
		"{}/prompt.root".format(input_dir),
	    "{}/qflip.root".format(input_dir),
	    "{}/photon.root".format(input_dir),
	    ]

	# background file names
	#sig_fnames = [
	#    "{}/www.root".format(input_dir),
	#    "{}/wwz.root".format(input_dir),
	#    "{}/wzz.root".format(input_dir), 
	#    "{}/zzz.root".format(input_dir),
	#	]
	sig_fnames = [
	    "{}/vvv.root".format(input_dir),
		]

	# get histos
	data  = getMultipleSRHisto(data_fname ,srs,selname,name)
	bgs   = getMultipleSRHistos(bkg_fnames,srs,selname,name)
	sigs  = getMultipleSRHistos(sig_fnames,srs,selname,name)
 

	legend_labels = [
		"Lost/three leptons",
		"Nonprompt lepton",
		"Irreducible",
		"Charge misassignment",
		"#gamma#rightarrowleptons",
		]
	#signal_labels = [
	#	"WWW",
	#	"WWZ",
	#	"WZZ",
	#	"ZZZ"
	#	]
	signal_labels = [
		"VVV",
		]

	# figure out extra text here
	txt = ""
	if "SRSS"		  in selname: txt = "2 same-sign leptons"
	if "SRSS2J" 	  in selname: txt = "SS N_{jet}=2"
	if "SRSSPreSel"   in selname: txt = "SS N_{jet}=2 preselection"
	if "SRSS1JPreSel" in selname: txt = "SS N_{jet}=1 preselection"
	if "SR0SFOS"      in selname: txt = "0SFOS channel"
	if "WZCRSS"       in selname: txt = "SS N_{jet}=2 WZ control region"
	if "CRBTag0SFOS"  in selname: txt = "0SFOS b-tag control region"
	if "CRBTagSS"     in selname: txt = "SS N_{jet}=2 b-tag control region"
	if "CRBTagSS1J"   in selname: txt = "SS N_{jet}=1 b-tag control region"

	histname = "{}__{}".format(selname,name)
	options = {
		"output_name": dirname + "/" + histname + ".png",
		"do_ratio": True,
		"stack_sig": True,
		"extra_text": txt,
		}
	options.update(extraoptions)

	histname = "{}__{}".format(selname,name)
	makePlot1D( histname, data, sigs, signal_labels, bgs, legend_labels, options )

	return 


def makeSS2Jplots(dirname):
	#
	# 2j SS Kin selection 
	#
	#srs = ["SRSSeeKinSel","SRSSemKinSel","SRSSmmKinSel"]
	#sel = "SRSSKinSel"
	srs = ["SRSSeePreSel","SRSSemPreSel","SRSSmmPreSel"]
	sel = "SRSSPreSel"
	#srs = ["SRSSee","SRSSem","SRSSmm"]
	#sel = "SRSS"

	# MjjL
	options = {
	 "yaxis_label": "Events",
	 "xaxis_label": "M_{jj} [GeV]",
	 "nbins": 25,
	 "xaxis_range": [0,500]
	}
	makePlotMultipleSRs(srs, sel, "MjjL" , dirname, options)

	# MjjL
	options = {
	 "yaxis_label": "Events",
	 "xaxis_label": "M_{jj} [GeV]",
	 "nbins": 15,
	}
	makePlotMultipleSRs(srs, sel, "Mjj" , dirname, options)

	# MET 
	options = {
	 "yaxis_label": "Events",
	 "xaxis_label": "E_{T}^{miss} [GeV]",
	 "nbins": 15,
	}
	makePlotMultipleSRs(srs, sel, "MET" , dirname, options)
	
	#MTmax 
	options = {
	 "yaxis_label": "Events",
	 "xaxis_label": "M_{T}^{max} [GeV]",
	 "nbins": 15,
	}
	makePlotMultipleSRs(srs, sel, "MTmax" , dirname, options)

	# DetajjL
	options = {
	 "yaxis_label": "Events",
	 "xaxis_label": "#Delta#eta(j,j)",
	 "nbins": 20,
	}
	makePlotMultipleSRs(srs, sel, "DetajjL" , dirname, options)
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

	# jet pT 
	options = {
	 "yaxis_label": "Events",
	 "xaxis_label": "p_{T}^{jet} [GeV]",
	 "nbins": 25,
	 "xaxis_range": [30,150]
	}
	makePlotMultipleSRs(srs, sel, "jets_pt0" , dirname, options)

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

	# M3l 
	options = {
	 "yaxis_label": "Events",
	 #"yaxis_range": [0,40],
	 "xaxis_label": "m(3l) [GeV]",
	 "nbins": 15,
	}
	makePlotMultipleSRs(srs, sel, "M3l" , dirname, options)


	# dR3lmet
	options = {
	 "yaxis_label": "Events",
	 "yaxis_range": [0,30],
	 "xaxis_label": "#Delta#phi(3l,p_{T}^{miss}) [GeV]",
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
	makePlotMultipleSRs(srs, sel, "MjjL" , dirname, options)

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

	# lead lep pT 
	options = {
	 "yaxis_label": "Events",
	# "yaxis_range": [0,50],
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

	# min dR j
	options = {
	 "yaxis_label": "Events",
	 #"yaxis_range": [0,35],
	 "xaxis_label": "min #DeltaR(l,j)",
	 "nbins": 15,
	 #"xaxis_range": [0,4.0],
	}
	makePlotMultipleSRs(srs, sel, "DRljmin3L" , dirname, options)

	# SS 1J 
	srs = ["CRBTag1Jee1JPre", "CRBTag1Jem1JPre", "CRBTag1Jmm1JPre"]
	sel = "CRBTag1JPre"
	makePlotMultipleSRs(srs, sel, "DRljmin" , dirname, options)

	return 

def makeSSinclusive(dirname):
	#
	# 3l - preselelctin
	#
	srs = ["SRSSee","SRSSem","SRSSmm"]
	sel = "SRSS"
	
	options = {
	 "yaxis_label": "Events",
	 "xaxis_label": "N_{jets}",
	 "xaxis_range": [0,5],
	 "xaxis_bin_text_labels": ["0","1","2","3","4"],
	}
	makePlotMultipleSRs(srs, sel, "nj" , dirname, options)
	
	options = {
	 "yaxis_label": "Events",
	 "xaxis_label": "N_{b-jets}",
	 "ratio_ndivisions" : 505,
	 "xaxis_ndivisions" : 505,
	 "xaxis_range": [0,4],
	 "xaxis_bin_text_labels": ["0","1","2","3"],
	}
	makePlotMultipleSRs(srs, sel, "nb" , dirname, options)
	
	options = {
	 "yaxis_label": "Events",
	 "xaxis_label": "p_{T}^{ll} [GeV]",
	 "nbins": 20
	}
	makePlotMultipleSRs(srs, sel, "Ptll" , dirname, options)

	options = {
	 "yaxis_label": "Events",
	 "xaxis_label": "M_{jj} [GeV]",
	 "nbins": 20,
	 "xaxis_range": [0,500]
	}
	sel = "SRSS2J"
	makePlotMultipleSRs(srs, sel, "MjjL" , dirname, options)

	return 

# Plot things...
dirname = "plots"
makeSSinclusive(dirname)
makeSS2Jplots(dirname)
makeSS1Jplots(dirname)
make0SFOSplots(dirname)

makeWZCRSSplots(dirname)
makeFakeCRplots(dirname)



# test 


