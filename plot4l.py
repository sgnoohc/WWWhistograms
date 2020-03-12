import ROOT

from style import *
from ratio import *
from comparison import *

setStyle()

def makePlotMultipleSRs_4lep(srs, selname, name , dirname, extraoptions={}):


	input_dir = "/nfs-7/userdata/phchang/vvvauxplots/outputs/WVZMVA2016_v0.1.21_WVZMVA2017_v0.1.21_WVZMVA2018_v0.1.21/y2016_v9_nom_y2017_v9_nom_y2018_v9_nom/"
	
	data_fname = "{}/data.root".format(input_dir)
	
	bkg_fnames = [
		"{}/zz.root".format(input_dir),
		"{}/ttz.root".format(input_dir), # may want to take fakes from data
		"{}/twz.root".format(input_dir),
	    "{}/wz.root".format(input_dir),
	    "{}/other.root".format(input_dir),
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
		"ZZ",
		"t#bar{t}Z",
		"tWZ",
		"WZ",
		"Other",
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
	if "ChannelOnZ"		  in selname: txt = "ZZ control region"
	if "ChannelBTagEMu"		  in selname: txt = "n_{b} #geq 1 t#bar{t}Z control region"

	histname = "{}__{}".format(selname,name)
	options = {
		"output_name": dirname + "/" + histname + "_ratio.png",
		"do_ratio": True,
		"stack_sig": True,
		"extra_text": txt,
		}
	options.update(extraoptions)
	if "nb" in name: 
		options.update({"yaxis_title_offset": 1.2})
		options.update({"ratio_yaxis_title_offset": 0.4})

	makePlot1Dratio( histname, data, sigs, signal_labels, bgs, legend_labels, options )

	options = {
		"output_name": dirname + "/" + histname + "_compare.png",
		"do_ratio": False,
		"stack_sig": False,
		"extra_text": txt,
		}
	options.update(extraoptions)
	if "nb" in name: options.update({"yaxis_title_offset": 1.4})

	makePlot1D( histname, data, sigs, signal_labels, bgs, legend_labels, options )

	return 

def makeZZCR4Lplots(dirname):
	#
	# 3l - preselelctin
	#
	srs = ["ChannelOnZ"]
	sel = "ChannelOnZ"
	scale = 5

	# MTmax 
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 #"yaxis_range": [0,25],
	 "xaxis_label": "m_{ll} [GeV]",
	 "nbins": 45,
	}
	makePlotMultipleSRs_4lep(srs, sel, "MET" , dirname, options)

def makePlotMultipleSRs_56lep(srs, selname, name , dirname, extraoptions={}):

	input_dir = "/nfs-7/userdata/phchang/vvvauxplots/56L_y2016_20200312_v1_y2017_20200312_v1_y2018_20200312_v1"
	
	data_fname = "{}/data.root".format(input_dir)
	
	bkg_fnames = [
		"{}/zz.root".format(input_dir),
		"{}/nonzz.root".format(input_dir),
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
		"ZZ",
		"Other",
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

# FiveLeptons__MT5th, FiveLeptons__ZcandidateOne, FiveLeptons__ZcandidateTwo, SixLeptons__SumPt

	# figure out extra text here
	txt = ""
	if "FiveLeptons"		  in selname: txt = "5 leptons preselection"
	if "SixLeptons"		  in selname: txt = "6 leptons preselection"

	histname = "{}__{}".format(selname,name)
	options = {
		"output_name": dirname + "/" + histname + "_ratio.png",
		"do_ratio": True,
		"stack_sig": True,
		"extra_text": txt,
		}
	options.update(extraoptions)
	if "nb" in name: 
		options.update({"yaxis_title_offset": 1.2})
		options.update({"ratio_yaxis_title_offset": 0.4})

	makePlot1Dratio( histname, data, sigs, signal_labels, bgs, legend_labels, options )

	options = {
		"output_name": dirname + "/" + histname + "_compare.png",
		"do_ratio": False,
		"stack_sig": False,
		"extra_text": txt,
		}
	options.update(extraoptions)
	if "nb" in name: options.update({"yaxis_title_offset": 1.4})

	makePlot1D( histname, data, sigs, signal_labels, bgs, legend_labels, options )

	return 

def make56Lplots(dirname):
	#
	# 5l
	#
	srs = ["FiveLeptons"]
	sel = "FiveLeptons"
	scale = 1

	# MTmax 
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 #"yaxis_range": [0,25],
	 "xaxis_label": "m_{T,5th} [GeV]",
	 "nbins": 20,
	}
	makePlotMultipleSRs_56lep(srs, sel, "MT5th" , dirname, options)

	#
	# 6l
	#
	srs = ["SixLeptons"]
	sel = "SixLeptons"
	scale = 1

	# MTmax 
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "yaxis_range": [0,0.15],
	 "xaxis_label": "#Sigma p_{T,lep} [GeV]",
	 "nbins": 20,
	}
	makePlotMultipleSRs_4lep(srs, sel, "SumPt" , dirname, options)

dirname = "plots_4l"

makeZZCR4Lplots(dirname)



