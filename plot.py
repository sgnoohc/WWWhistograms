import ROOT

from style import *
from ratio import *
from comparison import *

setStyle()






def makePlotMultipleSRs(srs, selname, name , dirname, extraoptions={}):


	input_dir = "/nfs-7/userdata/kdipetri/WWWhists/combineyearsLoose_v5.3.3/2020_03_09_1500/"
	
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
	if "SRSS2J" 	  in selname: txt = "SS n_{j}=2"
	if "SRSSPreSel"   in selname: txt = "SS n_{j}=2 preselection"
	if "SRSSKinSel"	  in selname: txt = "SS n_{j}=2 SRs" 
	if "SRSSKinSelnoee"	  in selname: txt = "SS n_{j}=2 e#mu #mu#mu SRs" 
	if "SRSS1JPreSel" in selname: txt = "SS n_{j}=1 preselection"
	if "SR0SFOS"      in selname: txt = "0SFOS channel"
	if "WZCRSS"       in selname: txt = "SS n_{j}=2 WZ control region"
	if "CRBTag0SFOS"  in selname: txt = "0SFOS b-tag control region"
	if "CRBTagSS"     in selname: txt = "SS n_{j}=2 b-tag control region"
	if "CRBTagSS1J"   in selname: txt = "SS n_{j}=1 b-tag control region"

	if "SR2SFOSPreSel" in selname : txt = "2SFOS preselection"
	if "SR1SFOSPreSel" in selname : txt = "1SFOS preselection"
	if "SR0SFOSPreSel" in selname : txt = "0SFOS preselection"
	
	if "SR2SFOSPreSelBDT" in selname : txt = "2SFOS BDT preselection"
	if "SR1SFOSPreSelBDT" in selname : txt = "1SFOS BDT preselection"
	if "SR0SFOSPreSelBDT" in selname : txt = "0SFOS BDT preselection"
	if "SRSSPreSelBDT" in selname : txt = "SS n_{j}=2 BDT preselection"

	if "Cut3LPreSel" in selname : txt = "3L preselection"

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


def makeSS2Jplots(dirname):
	#
	# 2j SS Kin selection 
	#

	srs = ["SRSSeePreSel","SRSSemPreSel","SRSSmmPreSel"]
	sel = "SRSSPreSel"
	scale = 15

	# MET 
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "xaxis_label": "p_{T}^{miss} [GeV]",
	 #"yaxis_range": [0,220],
	 "nbins": 20,
	}
	makePlotMultipleSRs(srs, sel, "METWide" , dirname, options)
	
	#MTmax 
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "xaxis_label": "m_{T}^{max} [GeV]",
	 "nbins": 15,
	}
	makePlotMultipleSRs(srs, sel, "MTmax" , dirname, options)

	# DetajjL
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "xaxis_label": "#Delta#eta(j,j)",
	 "nbins": 20,
	}
	makePlotMultipleSRs(srs, sel, "DetajjL" , dirname, options)

	# Mjj
	srs = ["SRSSeeKinSel","SRSSemKinSel","SRSSmmKinSel"]
	sel = "SRSSKinSel"
	options = {
	 "signal_scale": 5,
	 "yaxis_label": "Events",
	 "xaxis_label": "m_{jj} [GeV]",
	 "nbins": 10,
	 #"xaxis_range": [0,500]
	}
	makePlotMultipleSRs(srs, sel, "Mjj" , dirname, options)

	return


def makeSS1Jplots(dirname):
	#
	# 1j - SS Preselection
	# 
	srs = ["SRSS1Jee1JPre","SRSS1Jem1JPre","SRSS1Jmm1JPre"]
	sel = "SRSS1JPreSel"
	scale = 20
	
	# MET 
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "xaxis_label": "p_{T}^{miss} [GeV]",
	 "nbins": 15,
	}
	makePlotMultipleSRs(srs, sel, "MET" , dirname, options)
	
	# min mlj
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 #"yaxis_range": [0,35],
	 "xaxis_label": "m_{lj}^{min} [GeV]",
	 "nbins": 10,
	 "yaxis_range": [0,500],
	}
	makePlotMultipleSRs(srs, sel, "Mljmin" , dirname, options)

	# min DRlj
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 #"yaxis_range": [0,35],
	 "xaxis_label": "#DeltaR_{lj}^{min}",
	 "nbins": 25,
	 #"xaxis_range": [0,4.0],
	}
	makePlotMultipleSRs(srs, sel, "DRljmin" , dirname, options)
	
	# MTmax 
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "xaxis_label": "m_{T}^{max} [GeV]",
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

	scale = 2

	# MTmax 
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "yaxis_range": [0,25],
	 "xaxis_label": "m_{T}^{max} [GeV]",
	 "nbins": 15,
	}
	makePlotMultipleSRs(srs, sel, "MTmax" , dirname, options)

	# pT3l
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "yaxis_range": [0,40],
	 "xaxis_label": "p_{T}^{max}(3l) [GeV]",
	 "nbins": 15,
	}
	makePlotMultipleSRs(srs, sel, "Pt3l" , dirname, options)

	# M3l 
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 #"yaxis_range": [0,40],
	 "xaxis_label": "m(3l) [GeV]",
	 "nbins": 15,
	}
	makePlotMultipleSRs(srs, sel, "M3l" , dirname, options)

	srs = ["SR0SFOS"]
	sel = "SR0SFOS"
	scale = 2
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "xaxis_label": "n_{b}",
	 "xaxis_range": [0,4],
	 "xaxis_bin_text_labels": ["0","1","2","3"],
	}
	makePlotMultipleSRs(srs,sel,"nb", dirname, options)

	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "xaxis_label": "prompt BDT score",
	 "nbins": 10
	 #"xaxis_range": [0,4],
	 #"xaxis_bin_text_labels": ["0","1","2","3"],
	}
	makePlotMultipleSRs(srs,sel,"BDT_lostlep_prompt_SFOS", dirname, options)
	
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "xaxis_label": "#gamma-fake BDT score",
	 "nbins": 10
	 #"xaxis_range": [0,4],
	 #"xaxis_bin_text_labels": ["0","1","2","3"],
	}
	makePlotMultipleSRs(srs,sel,"BDT_photon_fakes_SFOS_noBtag", dirname, options)
	return 

def makeWZCRSSplots(dirname):
	#
	# 3l - preselelctin
	#
	srs = ["WZCRSSeePreSel","WZCRSSemPreSel","WZCRSSmmPreSel"]
	sel = "WZCRSSPreSel"
	scale = 5

	# MTmax 
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 #"yaxis_range": [0,25],
	 "xaxis_label": "m_{jj} [GeV]",
	 "nbins": 20,
	}
	makePlotMultipleSRs(srs, sel, "Mjj" , dirname, options)

	# mT third
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 #"yaxis_range": [0,25],
	 "xaxis_label": "m_{T}^{3rd} [GeV]",
	 "nbins": 20,
	}
	makePlotMultipleSRs(srs, sel, "MT3rd" , dirname, options)

	# mT max
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 #"yaxis_range": [0,25],
	 "xaxis_label": "m_{T}^{max} [GeV]",
	 "nbins": 20,
	}
	makePlotMultipleSRs(srs, sel, "MTmax" , dirname, options)

	# SFOS
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 #"yaxis_range": [0,25],
	 "xaxis_label": "m_{ll}^{SFOS} [GeV]",
	 "xaxis_range": [70,110],
	 "nbins": 50,
	}
	makePlotMultipleSRs(srs, sel, "MllOnOff" , dirname, options)

	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "xaxis_label": "prompt BDT score",
	 "nbins": 40,
	}
	makePlotMultipleSRs(srs,sel,"BDT_lostlep_prompt_SFOS", dirname, options)


	return 

def makeFakeCRplots(dirname):
	#
	# 3l - preselelctin
	#
	srs = ["CRBTageePreSel","CRBTagmmPreSel","CRBTagmmPreSel"]
	sel = "CRBTagPreSel"

	srs = ["CRBTag0SFOS"]
	sel = "CRBTag0SFOS"

	scale = 5
	# trying tighter
	#srs = ["CRBTageeKinSel","CRBTagmmKinSel","CRBTagmmKinSel"]
	#sel = "CRBTagKinSel"

	# lead lep pT 
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	# "yaxis_range": [0,50],
	 "xaxis_label": "Leading lepton p_{T} [GeV]",
	 "nbins": 10,
	}
	makePlotMultipleSRs(srs, sel, "lep_pt0" , dirname, options)

	# MT
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "yaxis_range": [0,35],
	 "xaxis_label": "m_{T}^{max} [GeV]",
	 "nbins": 10,
	}
	makePlotMultipleSRs(srs, sel, "MTmax" , dirname, options)

	# SS 1J 
	srs = ["CRBTag1Jee1JPre", "CRBTag1Jem1JPre", "CRBTag1Jmm1JPre"]
	sel = "CRBTagSS1JPreSel"
	# min dR j
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 #"yaxis_range": [0,35],
	 "xaxis_label": "m_{lj}^{min}",
	 "nbins": 15,
	 #"xaxis_range": [0,4.0],
	}
	makePlotMultipleSRs(srs, sel, "Mljmin" , dirname, options)

	# min dR j
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 #"yaxis_range": [0,35],
	 "xaxis_label": "#DeltaR_{lj}^{min}",
	 "nbins": 15,
	 #"xaxis_range": [0,4.0],
	}
	makePlotMultipleSRs(srs, sel, "DRljmin" , dirname, options)

	# SS 1J 
	#srs = ["CRBTagee", "CRBTagem", "CRBTagmm"]
	srs = ["CRBTageePreSelBDT", "CRBTagemPreSelBDT", "CRBTagmmPreSelBDT"]
	sel = "CRBTagSS2JPreSel"
	

	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "xaxis_label": "#gamma-fake BDT score",
	 "nbins": 20,
	}
	makePlotMultipleSRs(srs,sel,"BDT_photon_fakes_SFOS_noBtag", dirname, options)

	return 

def makeSSinclusive(dirname):
	#
	# 3l - preselelctin
	#
	srs = ["SRSSee","SRSSem","SRSSmm"]
	sel = "SRSS"
	scale = 30
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "xaxis_label": "n_{j}",
	 "xaxis_range": [0,5],
	 "xaxis_bin_text_labels": ["0","1","2","3","4"],
	}
	makePlotMultipleSRs(srs, sel, "nj" , dirname, options)
	
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "xaxis_label": "n_{b}",
	 "ratio_ndivisions" : 505,
	 "xaxis_ndivisions" : 505,
	 "xaxis_range": [0,4],
	 "xaxis_bin_text_labels": ["0","1","2","3"],
	}
	makePlotMultipleSRs(srs, sel, "nb" , dirname, options)
	
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "xaxis_label": "p_{T}^{ll} [GeV]",
	 "nbins": 20
	}
	makePlotMultipleSRs(srs, sel, "Ptll" , dirname, options)

	# min mlj
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 #"yaxis_range": [0,35],
	 "xaxis_label": "#DeltaR_{lj}^{min} [GeV]",
	 "nbins": 20,
	 #"yaxis_range": [0,500],
	}
	makePlotMultipleSRs(srs, sel, "DRljmin" , dirname, options)

	return 

def makeBDTPlots():
	
	## SS BDTs
	srs = ["SRSSeePreSelBDT","SRSSemPreSelBDT","SRSSmmPreSelBDT"]
	sel = "SRSSPreSelBDT"
	scale = 20

	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "xaxis_label": "prompt BDT score",
	 "nbins": 20,
	}
	makePlotMultipleSRs(srs,sel,"BDT_lostlep_prompt_SS2J", dirname, options)

	scale = 10
	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "xaxis_label": "#gamma-fake BDT score",
	 "nbins": 15,
	}
	makePlotMultipleSRs(srs,sel,"BDT_photon_fakes_SS2J_noBtag", dirname, options)

	## SS BDTs
	srs = ["SR0SFOS"]
	sel = "SR0SFOS"
	scale = 2

	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "xaxis_label": "prompt BDT score",
	 "nbins": 10,
	}
	makePlotMultipleSRs(srs,sel,"BDT_lostlep_prompt_SFOS", dirname, options)

	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "xaxis_label": "#gamma-fake BDT score",
	 "nbins": 10,
	}
	makePlotMultipleSRs(srs,sel,"BDT_photon_fakes_SFOS_noBtag", dirname, options)

	## SS BDTs
	srs = ["SR1SFOSPreSelBDT"]
	sel = "SR1SFOSPreSelBDT"
	scale = 50

	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "xaxis_label": "prompt BDT score",
	 "nbins": 20,
	}
	makePlotMultipleSRs(srs,sel,"BDT_lostlep_prompt_SFOS", dirname, options)

	options = {
	 "signal_scale" : scale,
	 "yaxis_label": "Events",
	 "xaxis_label": "#gamma-fake BDT score",
	 "nbins": 20,
	}
	makePlotMultipleSRs(srs,sel,"BDT_photon_fakes_SFOS_noBtag", dirname, options)

	return


# Plot things...
dirname = "plots"



srs = ["SR0SFOSPreSel","SR1SFOSPreSel","SR2SFOSPreSel"]
sel = "Cut3LPreSel"
scale = 100

options = {
 "signal_scale" : scale,
 "yaxis_label": "Events",
 #"yaxis_log": True,
 "xaxis_range": [0,3],
 "xaxis_bin_text_labels": ["0","1","2"],
}
makePlotMultipleSRs(srs,sel,"nSFOS", dirname, options)


options = {
 "signal_scale" : scale,
 "yaxis_label": "Events",
 "xaxis_label":"p_{T}^{lll}",
 "xaxis_range":[0,200],
 "nbins": 40,
 #"yaxis_log": True,
}
makePlotMultipleSRs(srs,sel,"Pt3l", dirname, options)

srs = ["SR1SFOSPreSel"]
sel = "SR1SFOSPreSel"
scale = 100

options = {
 "signal_scale" : scale,
 "yaxis_label": "Events",
 "xaxis_label":"m_{T}^{3rd}",
 #"xaxis_range":[0,200],
 "nbins": 30,
 #"yaxis_log": True,
}
makePlotMultipleSRs(srs,sel,"MT3rd", dirname, options)

srs = ["SR2SFOSPreSel"]
sel = "SR2SFOSPreSel"
scale = 100

options = {
 "signal_scale" : scale,
 "yaxis_label": "Events",
 "xaxis_label":"m_{T}^{max}",
 #"xaxis_range":[0,200],
 "nbins": 30,
 #"yaxis_log": True,
}
makePlotMultipleSRs(srs,sel,"MTmax", dirname, options)


srs = ["SR2SFOSPreSel"]
sel = "SR2SFOSPreSel"
scale = 100
options = {
 "signal_scale" : scale,
 "yaxis_label": "Events",
 "xaxis_label":"#Delta#phi(3l,p_{T}^{miss})",
 #"xaxis_range":[0,200],
 "nbins": 20,
 #"yaxis_log": True,
}
makePlotMultipleSRs(srs,sel,"DPhi3lMET", dirname, options)

options = {
 "signal_scale" : scale,
 "yaxis_label": "Events",
 "xaxis_label":"p_{T}^{lll}",
 "xaxis_range":[0,200],
 "nbins": 40,
 #"yaxis_log": True,
}
makePlotMultipleSRs(srs,sel,"Pt3l", dirname, options)



#makeSSinclusive(dirname)
#makeSS2Jplots(dirname)
#makeSS1Jplots(dirname)
#make0SFOSplots(dirname)

#makeBDTPlots()

#makeWZCRSSplots(dirname)
makeFakeCRplots(dirname)

# BDT options
#  KEY: TH1F	SRSSmm__BDT_lostlep_prompt_SFOS;1	
#  KEY: TH1F	SRSSmm__BDT_lostlep_prompt_SS1J;1	
#  KEY: TH1F	SRSSmm__BDT_lostlep_prompt_SS2J;1	
#  KEY: TH1F	SRSSmm__BDT_photon_fakes_SFOS_noBtag;1	
#  KEY: TH1F	SRSSmm__BDT_photon_fakes_SS1J_noBtag;1	
#  KEY: TH1F	SRSSmm__BDT_photon_fakes_SS2J_noBtag;1	


# test 


