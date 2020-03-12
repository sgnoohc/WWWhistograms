
import ROOT

from style import *


def makePlot1Dratio( histname, data, sigs, signal_labels, bgs, legend_labels , options ): #, _persist = []):

	opts = Options(options, kind="1dratio")

	
	if opts["canvas_width"] and opts["canvas_height"]:
	    width = opts["canvas_width"]
	    height = opts["canvas_height"]
	    c1 = ROOT.TCanvas(histname+"ratio", "", width, height)
	else: 
		c1 = ROOT.TCanvas(histname+"ratio","")
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
	if opts["yaxis_ndivisions"] : stack.GetYaxis().SetNdivisions( opts["yaxis_ndivisions"])

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
	draw_cms_lumi(c1, 0.035, opts)
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
	if len(bgs) > 2:
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
