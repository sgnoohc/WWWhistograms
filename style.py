import ROOT
import os
from array import array

def setStyle(): 
	ROOT.gROOT.SetBatch(1) # please don't open an Xwindow
	ROOT.gStyle.SetOptStat(0)
	return 


class OptionsCompare(object):
    """
    The Options object is just a nice wrapper around a dictionary
    with default values, some arithmetic, and warnings
    >>> import plottery as ply
    >>> # Passing d_opts1,d_opts2, or opts1 as the `options` kwarg to a plot
    >>> # function will have the same effect
    >>> d_opts1 = { "output_name": "test.pdf", "blah": 1, }
    >>> d_opts2 = { "blah2": 2, }
    >>> opts1 = ply.Options(d_opts1)
    >>> # You can add a dict or another Options object to an Options object
    >>> # to add new options or modify current ones
    >>> print opts1+d_opts2
    >>> print opts1+ply.Options(d_opts2)
    """

    def __init__(self, options={}, kind=None):

        # if we pass in a plain dict, then do the usual
        # thing, otherwise make a new options object
        # if an Options object is passed in
        if type(options) is dict:
            self.options = options
            self.kind = kind
        else:
            self.options = options.options
            self.kind = options.kind

        self.recognized_options = {

            # Canvas
            "signal_scale": {"type": "Int", "desc": "width of TCanvas in pixel", "default": 10, "kinds": ["1dratio","graph","2d"], },


            "canvas_width": {"type": "Int", "desc": "width of TCanvas in pixel", "default": 800, "kinds": ["1dratio","graph","2d"], },
            "canvas_height": {"type": "Int", "desc": "height of TCanvas in pixel", "default": 800, "kinds": ["1dratio","graph","2d"], },
            "canvas_main_y1": {"type": "Float", "desc": "main plot tpad y1", "default": 0.28, "kinds": ["1dratio","graph","2d"], },
            "canvas_main_topmargin": {"type": "Float", "desc": "ratio plot top margin", "default": 0.1, "kinds": ["1dratio"], },
            "canvas_main_bottommargin": {"type": "Float", "desc": "ratio plot bottom margin", "default": 0.16, "kinds": ["1dratio"], },
            "canvas_main_rightmargin": {"type": "Float", "desc": "ratio plot right margin", "default": 0.05, "kinds": ["1dratio"], },
            "canvas_main_leftmargin": {"type": "Float", "desc": "ratio plot left margin", "default": 0.2, "kinds": ["1dratio"], },
            "canvas_ratio_y2": {"type": "Float", "desc": "ratio tpad y2", "default": 0.28, "kinds": ["1dratio","graph","2d"], },
            "canvas_ratio_topmargin": {"type": "Float", "desc": "ratio plot top margin", "default": 0.05, "kinds": ["1dratio"], },
            "canvas_ratio_bottommargin": {"type": "Float", "desc": "ratio plot bottom margin", "default": 0.4, "kinds": ["1dratio"], },
            "canvas_ratio_rightmargin": {"type": "Float", "desc": "ratio plot right margin", "default": 0.05, "kinds": ["1dratio"], },
            "canvas_ratio_leftmargin": {"type": "Float", "desc": "ratio plot left margin", "default": 0.16, "kinds": ["1dratio"], },
            "canvas_tick_one_side": {"type": "Boolean", "desc": "ratio plot left margin", "default": False, "kinds": ["1dratio"], },

            # Legend
            "legend_coordinates": { "type": "List", "desc": "4 elements specifying TLegend constructor coordinates", "default": [0.63,0.67,0.93,0.87], "kinds": ["1dratio","graph"], },
            "legend_alignment": { "type": "String", "desc": "easy alignment of TLegend. String containing two words from: bottom, top, left, right", "default": "", "kinds": ["1dratio","graph"], },
            "legend_smart": { "type": "Boolean", "desc": "Smart alignment of legend to prevent overlaps", "default": True, "kinds": ["1dratio"], },
            "legend_border": { "type": "Boolean", "desc": "show legend border?", "default": True, "kinds": ["1dratio","graph"], },
            "legend_rounded": { "type": "Boolean", "desc": "rounded legend border", "default": True, "kinds": ["1dratio"], },
            "legend_scalex": { "type": "Float", "desc": "scale width of legend by this factor", "default": 1, "kinds": ["1dratio","graph"], },
            "legend_scaley": { "type": "Float", "desc": "scale height of legend by this factor", "default": 1, "kinds": ["1dratio","graph"], },
            "legend_opacity": { "type": "Float", "desc": "from 0 to 1 representing the opacity of the TLegend white background", "default": 0.5, "kinds": ["1dratio","graph"], },
            "legend_ncolumns": { "type": "Int", "desc": "number of columns in the legend", "default": 1, "kinds": ["1dratio","graph"], },
            "legend_column_separation": { "type": "Float", "desc": "column separation size", "default": None, "kinds": ["1dratio","graph"], },
            "legend_percentageinbox": { "type": "Boolean", "desc": "show relative process contributions as %age in the legend thumbnails", "default": True, "kinds": ["1dratio"], },
            "legend_datalabel": { "type": "String", "desc": "label for the data histogram in the legend", "default": "Data", "kinds": ["1dratio"], },

            # Axes
            "nbins": { "type": "Int", "desc": "number of bins", "default": None, "kinds": ["1dratio"], },

            "xaxis_log": { "type": "Boolean", "desc": "log scale x-axis", "default": False, "kinds": ["1dratio","graph","2d"], },
            "yaxis_log": { "type": "Boolean", "desc": "log scale y-axis", "default": False, "kinds": ["1dratio","graph","2d"], },
            "zaxis_log": { "type": "Boolean", "desc": "log scale z-axis", "default": False, "kinds": ["2d"], },

            "xaxis_label": { "type": "String", "desc": "label for x axis", "default": "", "kinds": ["1dratio","graph","2d"], },
            "yaxis_label": { "type": "String", "desc": "label for y axis", "default": "Events", "kinds": ["1dratio","graph","2d"], },
            "zaxis_label": { "type": "String", "desc": "label for z axis", "default": "", "kinds": ["2d"], },

            "xaxis_label_size": { "type": "Float", "desc": "size of fonts for x axis", "default": 0.045, "kinds": ["1dratio","graph","2d"], },
            "yaxis_label_size": { "type": "Float", "desc": "size of fonts for y axis", "default": 0.045, "kinds": ["1dratio","graph","2d"], },
            "zaxis_label_size": { "type": "Float", "desc": "size of fonts for z axis", "default": 0.045, "kinds": ["2d"], },

            "xaxis_title_size": { "type": "Float", "desc": "size of fonts for x axis title", "default": 0.065, "kinds": ["1dratio","graph","2d"], },
            "yaxis_title_size": { "type": "Float", "desc": "size of fonts for y axis title", "default": 0.065, "kinds": ["1dratio","graph","2d"], },

            "xaxis_title_offset": { "type": "Float", "desc": "offset of x axis title", "default": 1.0, "kinds": ["1dratio","graph","2d"], },
            "yaxis_title_offset": { "type": "Float", "desc": "offset of y axis title", "default": 1.3, "kinds": ["1dratio","graph","2d"], },

            "xaxis_label_offset_scale": { "type": "Float", "desc": "x axis tickmark labels offset", "default": 1.0, "kinds": ["1dratio","graph","2d"], },
            "yaxis_label_offset_scale": { "type": "Float", "desc": "y axis tickmark labels offset", "default": 1.0, "kinds": ["1dratio","graph","2d"], },

            "xaxis_tick_length_scale": { "type": "Float", "desc": "x axis tickmark length scale", "default": 1.0, "kinds": ["1dratio","graph","2d"], },
            "yaxis_tick_length_scale": { "type": "Float", "desc": "y axis tickmark length scale", "default": 1.0, "kinds": ["1dratio","graph","2d"], },

            "xaxis_moreloglabels": { "type": "Boolean", "desc": "show denser labels with logscale for x axis", "default": True, "kinds": ["1dratio","graph","2d"], },
            "yaxis_moreloglabels": { "type": "Boolean", "desc": "show denser labels with logscale for y axis", "default": True, "kinds": ["1dratio","graph","2d"], },
            "zaxis_moreloglabels": { "type": "Boolean", "desc": "show denser labels with logscale for z axis", "default": True, "kinds": ["1dratio","graph","2d"], },
            "xaxis_noexponents": { "type": "Boolean", "desc": "don't show exponents in logscale labels for x axis", "default": False, "kinds": ["1dratio","graph","2d"], },
            "yaxis_noexponents": { "type": "Boolean", "desc": "don't show exponents in logscale labels for y axis", "default": False, "kinds": ["1dratio","graph","2d"], },
            "zaxis_noexponents": { "type": "Boolean", "desc": "don't show exponents in logscale labels for z axis", "default": False, "kinds": ["1dratio","graph","2d"], },

            "yaxis_exponent_offset": { "type": "Float", "desc": "offset x10^n left or right", "default": 0.0, "kinds": ["1dratio"], },
            "yaxis_exponent_vertical_offset": { "type": "Float", "desc": "offset x10^n up or down", "default": 0.0, "kinds": ["1dratio"], },

            "yaxis_ndivisions": { "type": "Int", "desc": "SetNdivisions integer for y-axis", "default": 505, "kinds": ["1dratio", "graph", "2d"], },
            "xaxis_ndivisions": { "type": "Int", "desc": "SetNdivisions integer for x-axis", "default": 505, "kinds": ["1dratio", "graph", "2d"], },

            "xaxis_range": { "type": "List", "desc": "2 elements to specify x axis range", "default": [], "kinds": ["1dratio","graph","2d"], },
            "yaxis_range": { "type": "List", "desc": "2 elements to specify y axis range", "default": [], "kinds": ["1dratio","graph","2d"], },
            "zaxis_range": { "type": "List", "desc": "2 elements to specify z axis range", "default": [], "kinds": ["2d"], },

            "xaxis_bins":{"type":"List","desc":"List containing bin labels instead of text","default":[],"kinds":["1dratio","graph","2dratio"]},
            "xaxis_bin_text_labels":{"type":"List","desc":"List containing bin labels instead of text","default":[],"kinds":["1dratio","graph","2dratio"]},

            # Ratio
            "do_ratio": { "type": "Boolean", "desc": "draw ratio plot", "default": False, "kinds": ["1dratio"], },
            "ratio_name": { "type": "String", "desc": "name of ratio pad", "default": "Data/Pred.", "kinds": ["1dratio"], },
            "ratio_name_size": { "type": "Float", "desc": "size of the name on the ratio pad (e.g. data/MC)", "default": 0.18, "kinds": ["1dratio"], },
            "ratio_label_size": { "type": "Float", "desc": "XY-axis label size", "default": 0.12, "kinds": ["1dratio"], },
            "ratio_xaxis_title_offset": { "type": "Float", "desc": "offset to the x-axis titles", "default": 0.85, "kinds": ["1dratio"], },
            "ratio_yaxis_title_offset": { "type": "Float", "desc": "offset to the y-axis titles", "default": 0.35, "kinds": ["1dratio"], },            
            "ratio_xaxis_label_offset": { "type": "Float", "desc": "offset to the x-axis labels (numbers)", "default": None, "kinds": ["1dratio"], },
            "ratio_yaxis_label_offset": { "type": "Float", "desc": "offset to the y-axis labels (numbers)", "default": None, "kinds": ["1dratio"], }, 
            "ratio_range": { "type": "List", "desc": "pair for min and max y-value for ratio; default auto re-sizes to 3 sigma range", "default": [0,2], "kinds": ["1dratio"], },
            "ratio_horizontal_lines": { "type": "List", "desc": "list of y-values to draw horizontal line", "default": [1.], "kinds": ["1dratio"], },
            "ratio_chi2prob": { "type": "Boolean", "desc": "show chi2 probability for ratio", "default": False, "kinds": ["1dratio"], },
            "ratio_pull": { "type": "Boolean", "desc": "show pulls instead of ratios in ratio pad", "default": False, "kinds": ["1dratio"], },
            "ratio_pull_numbers": { "type": "Boolean", "desc": "show numbers for pulls, and mean/sigma", "default": False, "kinds": ["1dratio"], },
            "ratio_ndivisions": { "type": "Int", "desc": "SetNdivisions integer for ratio", "default": 510, "kinds": ["1dratio"], },
            "ratio_numden_indices": { "type": "List", "desc": "Pair of numerator and denominator histogram indices (from `bgs`) for ratio", "default": None, "kinds": ["1dratio"], },
            "ratio_binomial_errors": { "type": "Boolean", "desc": "Use binomial error propagation when computing ratio eror bars", "default": False, "kinds": ["1dratio"], },
            "ratio_tick_length_scale": { "type": "Float", "desc": "Tick length scale of ratio pads", "default": 1.0, "kinds": ["1dratio"], },

            # Overall
            "title": { "type": "String", "desc": "plot title", "default": "", "kinds": ["1dratio","graph","2d"], },
            "draw_points": { "type": "Boolean", "desc": "draw points instead of fill", "default": False, "kinds": ["1d","1dratio"], },
            "draw_option_2d": { "type": "String", "desc": "hist draw option", "default": "colz", "kinds": ["2d"], },
            "bkg_err_fill_style": { "type": "Int", "desc": "Error shade draw style", "default": 3345, "kinds": ["1d", "1dratio"], },
            "bkg_err_fill_color": { "type": "Int", "desc": "Error shade color", "default": None, "kinds": ["1d", "1dratio"], },
            "ratio_err_fill_style": { "type": "Int", "desc": "Error shade draw style", "default": 3345, "kinds": ["1d", "1dratio"], },
            "ratio_err_fill_color": { "type": "Int", "desc": "Error shade color", "default": None, "kinds": ["1d", "1dratio"], },

            # CMS things
            "cms_label": {"type": "String", "desc": "E.g., 'Preliminary'; default hides label", "default": "Preliminary", "kinds": ["1dratio","graph","2d"]},
            "lumi_value": {"type": "String", "desc": "E.g., 35.9; default hides lumi label", "default": "137", "kinds": ["1dratio","graph","2d"]},
            "lumi_unit": {"type": "String", "desc": "Unit for lumi label", "default": "fb", "kinds": ["1dratio","graph","2d"]},

            # Misc
            "stack_sig": { "type": "Boolean", "desc": "stack signals", "default": True, "kinds": ["1dratio"], },
            "do_stack": { "type": "Boolean", "desc": "stack histograms", "default": True, "kinds": ["1dratio"], },
            "palette_name": { "type": "String", "desc": "color palette: 'default', 'rainbow', 'susy', etc.", "default": "default", "kinds": ["2d"], },
            "show_bkg_errors": { "type": "Boolean", "desc": "show error bar for background stack", "default": False, "kinds": ["1dratio"], },
            "show_bkg_smooth": { "type": "Boolean", "desc": "show smoothed background stack", "default": False, "kinds": ["1dratio"], },
            "bkg_sort_method": { "type": "Boolean", "desc": "how to sort background stack using integrals: 'unsorted', 'ascending', or 'descending'", "default": 'ascending', "kinds": ["1dratio"], },
            "no_ratio": { "type": "Boolean", "desc": "do not draw ratio plot", "default": False, "kinds": ["1dratio"], },

            "max_digits": { "type": "Int", "desc": "integer for max digits", "default": 5, "kinds" : ["1dratio", "graph", "2d"], },


            "bin_text_size": { "type": "Float", "desc": "size of text in bins (TH2::SetMarkerSize)", "default": 1.7, "kinds": ["2d"], },
            "bin_text_format": { "type": "String", "desc": "format string for text in TH2 bins", "default": ".1f", "kinds": ["2d"], },
            "bin_text_smart": { "type": "Boolean", "desc": "change bin text color for aesthetics", "default": False, "kinds": ["2d"], },
            "bin_text_format_smart": { "type": "String", "desc": "python-syntax format string for smart text in TH2 bins taking value and bin error", "default": "{0:.0f}#pm{1:.0f}", "kinds": ["2d"], },

            "hist_line_none": { "type": "Boolean", "desc": "No lines for histograms, only fill", "default": False, "kinds": ["1dratio"], },
            "hist_line_black": { "type": "Boolean", "desc": "Black lines for histograms", "default": False, "kinds": ["1dratio"], },
            "hist_disable_xerrors": { "type": "Boolean", "desc": "Disable the x-error bars on data for 1D hists", "default": True, "kinds": ["1dratio"], },

            "extra_text": { "type": "List", "desc": "list of strings for textboxes", "default": [], "kinds": [ "1dratio","graph"], },
            "extra_text_size": { "type": "Float", "desc": "size for extra text", "default": 0.03, "kinds": [ "1dratio","graph"], },
            "extra_text_xpos": { "type": "Float", "desc": "NDC x position (0 to 1) for extra text", "default": 0.235, "kinds": [ "1dratio","graph"], },
            "extra_text_ypos": { "type": "Float", "desc": "NDC y position (0 to 1) for extra text", "default": 0.74, "kinds": [ "1dratio","graph"], },

            "extra_lines": { "type": "List", "desc": "list of upto 7-tuples (x1,y1,x2,y2,style,width,color) for lines", "default": [], "kinds": [ "1dratio","graph"], },

            "no_overflow": {"type":"Boolean","desc":"Do not plot overflow bins","default": False, "kinds" : ["1dratio"],},

            # Fun
            "us_flag": { "type": "Boolean", "desc": "show the US flag in the corner", "default": False, "kinds": ["1dratio","graph","2d"], },
            "us_flag_coordinates": { "type": "List", "desc": "Specify flag location with (x pos, y pos, size)", "default": [0.68,0.96,0.06], "kinds": ["1dratio","graph","2d"], },

            # Output
            "output_name": { "type": "String", "desc": "output file name/path", "default": "plot.pdf", "kinds": ["1dratio","graph","2d"], },
            "output_ic": { "type": "Boolean", "desc": "run `ic` (imgcat) on output", "default": False, "kinds": ["1dratio","graph","2d"], },
            "output_jsroot": { "type": "Boolean", "desc": "output .json for jsroot", "default": False, "kinds": ["1dratio","graph","2d"], },
            "output_diff_previous": { "type": "Boolean", "desc": "diff the new output file with the previous", "default": False, "kinds": ["1dratio","graph","2d"], },

        }

        self.check_options()

    def usage(self):

        for key,obj in sorted(self.recognized_options.items()):
            default = obj["default"]
            desc = obj["desc"]
            typ = obj["type"]
            kinds = obj["kinds"]
            if self.kind and self.kind not in kinds: continue
            if type(default) is str: default = '"{}"'.format(default)
            print("* `{}` [{}]\n    {} (default: {})".format(key,typ,desc,default))

    def check_options(self):
        for name,val in self.options.items():
            if name not in self.recognized_options:
                print(">>> Option {} not in list of recognized options".format(name))
            else:
                obj = self.recognized_options[name]
                if self.kind not in obj["kinds"]:
                    print(">>> Option {} isn't declared to work with plot type of '{}'".format(name, self.kind))
                else:
                    pass
                    # print ">>> Carry on mate ... {} is fine".format(name)

    def __getitem__(self, key):
        if key in self.options:
            return self.options[key]
        else:
            if key in self.recognized_options:
                return self.recognized_options[key]["default"]
            else:
                print(">>> Hmm, can't find {} anywhere. Typo or intentional?".format(key))
                return None

    def get(self, key, default=None):
        val = self.__getitem__(key)
        if not val: return default
        else: return val

    def is_default(self, key):
        """
        returns True if user has not overriden this particular option
        """
        default = None
        if key in self.recognized_options:
            default = self.recognized_options[key]["default"]
        return (self.__getitem__(key) == default)

    def __setitem__(self, key, value):
        self.options[key] = value

    def __repr__(self):
        return str(self.options)

    def __contains__(self, key):
        return key in self.options

    def __add__(self, other):
        new_opts = {}
        new_opts.update(self.options)
        if type(other) is dict:
            new_opts.update(other)
        else:
            new_opts.update(other.options)
        return Options(new_opts,kind=self.kind)

class Options(object):
    """
    The Options object is just a nice wrapper around a dictionary
    with default values, some arithmetic, and warnings
    >>> import plottery as ply
    >>> # Passing d_opts1,d_opts2, or opts1 as the `options` kwarg to a plot
    >>> # function will have the same effect
    >>> d_opts1 = { "output_name": "test.pdf", "blah": 1, }
    >>> d_opts2 = { "blah2": 2, }
    >>> opts1 = ply.Options(d_opts1)
    >>> # You can add a dict or another Options object to an Options object
    >>> # to add new options or modify current ones
    >>> print opts1+d_opts2
    >>> print opts1+ply.Options(d_opts2)
    """

    def __init__(self, options={}, kind=None):

        # if we pass in a plain dict, then do the usual
        # thing, otherwise make a new options object
        # if an Options object is passed in
        if type(options) is dict:
            self.options = options
            self.kind = kind
        else:
            self.options = options.options
            self.kind = options.kind

        self.recognized_options = {
			"signal_scale": {"type": "Int", "desc": "width of TCanvas in pixel", "default": None, "kinds": ["1dratio","graph","2d"], },


            # Canvas
            "canvas_width": {"type": "Int", "desc": "width of TCanvas in pixel", "default": 700, "kinds": ["1dratio","graph","2d"], },
            "canvas_height": {"type": "Int", "desc": "height of TCanvas in pixel", "default": 800, "kinds": ["1dratio","graph","2d"], },
            "canvas_main_y1": {"type": "Float", "desc": "main plot tpad y1", "default": 0.28, "kinds": ["1dratio","graph","2d"], },
            "canvas_main_topmargin": {"type": "Float", "desc": "ratio plot top margin", "default": 0.1, "kinds": ["1dratio"], },
            "canvas_main_bottommargin": {"type": "Float", "desc": "ratio plot bottom margin", "default": 0.05, "kinds": ["1dratio"], },
            "canvas_main_rightmargin": {"type": "Float", "desc": "ratio plot right margin", "default": 0.05, "kinds": ["1dratio"], },
            "canvas_main_leftmargin": {"type": "Float", "desc": "ratio plot left margin", "default": 0.16, "kinds": ["1dratio"], },
            "canvas_ratio_y2": {"type": "Float", "desc": "ratio tpad y2", "default": 0.28, "kinds": ["1dratio","graph","2d"], },
            "canvas_ratio_topmargin": {"type": "Float", "desc": "ratio plot top margin", "default": 0.05, "kinds": ["1dratio"], },
            "canvas_ratio_bottommargin": {"type": "Float", "desc": "ratio plot bottom margin", "default": 0.4, "kinds": ["1dratio"], },
            "canvas_ratio_rightmargin": {"type": "Float", "desc": "ratio plot right margin", "default": 0.05, "kinds": ["1dratio"], },
            "canvas_ratio_leftmargin": {"type": "Float", "desc": "ratio plot left margin", "default": 0.16, "kinds": ["1dratio"], },
            "canvas_tick_one_side": {"type": "Boolean", "desc": "ratio plot left margin", "default": False, "kinds": ["1dratio"], },

            # Legend
            "legend_coordinates": { "type": "List", "desc": "4 elements specifying TLegend constructor coordinates", "default": [0.63,0.67,0.93,0.87], "kinds": ["1dratio","graph"], },
            "legend_alignment": { "type": "String", "desc": "easy alignment of TLegend. String containing two words from: bottom, top, left, right", "default": "", "kinds": ["1dratio","graph"], },
            "legend_smart": { "type": "Boolean", "desc": "Smart alignment of legend to prevent overlaps", "default": True, "kinds": ["1dratio"], },
            "legend_border": { "type": "Boolean", "desc": "show legend border?", "default": True, "kinds": ["1dratio","graph"], },
            "legend_rounded": { "type": "Boolean", "desc": "rounded legend border", "default": True, "kinds": ["1dratio"], },
            "legend_scalex": { "type": "Float", "desc": "scale width of legend by this factor", "default": 1, "kinds": ["1dratio","graph"], },
            "legend_scaley": { "type": "Float", "desc": "scale height of legend by this factor", "default": 1, "kinds": ["1dratio","graph"], },
            "legend_opacity": { "type": "Float", "desc": "from 0 to 1 representing the opacity of the TLegend white background", "default": 0.5, "kinds": ["1dratio","graph"], },
            "legend_ncolumns": { "type": "Int", "desc": "number of columns in the legend", "default": 1, "kinds": ["1dratio","graph"], },
            "legend_column_separation": { "type": "Float", "desc": "column separation size", "default": None, "kinds": ["1dratio","graph"], },
            "legend_percentageinbox": { "type": "Boolean", "desc": "show relative process contributions as %age in the legend thumbnails", "default": True, "kinds": ["1dratio"], },
            "legend_datalabel": { "type": "String", "desc": "label for the data histogram in the legend", "default": "Data", "kinds": ["1dratio"], },

            # Axes
            "nbins": { "type": "Int", "desc": "number of bins", "default": None, "kinds": ["1dratio"], },

            "xaxis_log": { "type": "Boolean", "desc": "log scale x-axis", "default": False, "kinds": ["1dratio","graph","2d"], },
            "yaxis_log": { "type": "Boolean", "desc": "log scale y-axis", "default": False, "kinds": ["1dratio","graph","2d"], },
            "zaxis_log": { "type": "Boolean", "desc": "log scale z-axis", "default": False, "kinds": ["2d"], },

            "xaxis_label": { "type": "String", "desc": "label for x axis", "default": "", "kinds": ["1dratio","graph","2d"], },
            "yaxis_label": { "type": "String", "desc": "label for y axis", "default": "Events", "kinds": ["1dratio","graph","2d"], },
            "zaxis_label": { "type": "String", "desc": "label for z axis", "default": "", "kinds": ["2d"], },

            "xaxis_label_size": { "type": "Float", "desc": "size of fonts for x axis", "default": 0.045, "kinds": ["1dratio","graph","2d"], },
            "yaxis_label_size": { "type": "Float", "desc": "size of fonts for y axis", "default": 0.045, "kinds": ["1dratio","graph","2d"], },
            "zaxis_label_size": { "type": "Float", "desc": "size of fonts for z axis", "default": 0.045, "kinds": ["2d"], },

            "xaxis_title_size": { "type": "Float", "desc": "size of fonts for x axis title", "default": None, "kinds": ["1dratio","graph","2d"], },
            "yaxis_title_size": { "type": "Float", "desc": "size of fonts for y axis title", "default": 0.065, "kinds": ["1dratio","graph","2d"], },

            "xaxis_title_offset": { "type": "Float", "desc": "offset of x axis title", "default": None, "kinds": ["1dratio","graph","2d"], },
            "yaxis_title_offset": { "type": "Float", "desc": "offset of y axis title", "default": 1.0, "kinds": ["1dratio","graph","2d"], },

            "xaxis_label_offset_scale": { "type": "Float", "desc": "x axis tickmark labels offset", "default": 1.0, "kinds": ["1dratio","graph","2d"], },
            "yaxis_label_offset_scale": { "type": "Float", "desc": "y axis tickmark labels offset", "default": 1.0, "kinds": ["1dratio","graph","2d"], },

            "xaxis_tick_length_scale": { "type": "Float", "desc": "x axis tickmark length scale", "default": 1.0, "kinds": ["1dratio","graph","2d"], },
            "yaxis_tick_length_scale": { "type": "Float", "desc": "y axis tickmark length scale", "default": 1.0, "kinds": ["1dratio","graph","2d"], },

            "xaxis_moreloglabels": { "type": "Boolean", "desc": "show denser labels with logscale for x axis", "default": True, "kinds": ["1dratio","graph","2d"], },
            "yaxis_moreloglabels": { "type": "Boolean", "desc": "show denser labels with logscale for y axis", "default": True, "kinds": ["1dratio","graph","2d"], },
            "zaxis_moreloglabels": { "type": "Boolean", "desc": "show denser labels with logscale for z axis", "default": True, "kinds": ["1dratio","graph","2d"], },
            "xaxis_noexponents": { "type": "Boolean", "desc": "don't show exponents in logscale labels for x axis", "default": False, "kinds": ["1dratio","graph","2d"], },
            "yaxis_noexponents": { "type": "Boolean", "desc": "don't show exponents in logscale labels for y axis", "default": False, "kinds": ["1dratio","graph","2d"], },
            "zaxis_noexponents": { "type": "Boolean", "desc": "don't show exponents in logscale labels for z axis", "default": False, "kinds": ["1dratio","graph","2d"], },

            "yaxis_exponent_offset": { "type": "Float", "desc": "offset x10^n left or right", "default": 0.0, "kinds": ["1dratio"], },
            "yaxis_exponent_vertical_offset": { "type": "Float", "desc": "offset x10^n up or down", "default": 0.0, "kinds": ["1dratio"], },

            "yaxis_ndivisions": { "type": "Int", "desc": "SetNdivisions integer for y-axis", "default": 505, "kinds": ["1dratio", "graph", "2d"], },
            "xaxis_ndivisions": { "type": "Int", "desc": "SetNdivisions integer for x-axis", "default": 505, "kinds": ["1dratio", "graph", "2d"], },

            "xaxis_range": { "type": "List", "desc": "2 elements to specify x axis range", "default": [], "kinds": ["1dratio","graph","2d"], },
            "yaxis_range": { "type": "List", "desc": "2 elements to specify y axis range", "default": [], "kinds": ["1dratio","graph","2d"], },
            "zaxis_range": { "type": "List", "desc": "2 elements to specify z axis range", "default": [], "kinds": ["2d"], },

            "xaxis_bins":{"type":"List","desc":"List containing bin labels instead of text","default":[],"kinds":["1dratio","graph","2dratio"]},
            "xaxis_bin_text_labels":{"type":"List","desc":"List containing bin labels instead of text","default":[],"kinds":["1dratio","graph","2dratio"]},

            # Ratio
            "do_ratio": { "type": "Boolean", "desc": "draw ratio plot", "default": False, "kinds": ["1dratio"], },
            "ratio_name": { "type": "String", "desc": "name of ratio pad", "default": "Data/Pred.", "kinds": ["1dratio"], },
            "ratio_name_size": { "type": "Float", "desc": "size of the name on the ratio pad (e.g. data/MC)", "default": 0.18, "kinds": ["1dratio"], },
            "ratio_label_size": { "type": "Float", "desc": "XY-axis label size", "default": 0.12, "kinds": ["1dratio"], },
            "ratio_xaxis_title_offset": { "type": "Float", "desc": "offset to the x-axis titles", "default": 0.85, "kinds": ["1dratio"], },
            "ratio_yaxis_title_offset": { "type": "Float", "desc": "offset to the y-axis titles", "default": 0.35, "kinds": ["1dratio"], },            
            "ratio_xaxis_label_offset": { "type": "Float", "desc": "offset to the x-axis labels (numbers)", "default": None, "kinds": ["1dratio"], },
            "ratio_yaxis_label_offset": { "type": "Float", "desc": "offset to the y-axis labels (numbers)", "default": None, "kinds": ["1dratio"], }, 
            "ratio_range": { "type": "List", "desc": "pair for min and max y-value for ratio; default auto re-sizes to 3 sigma range", "default": [0,2], "kinds": ["1dratio"], },
            "ratio_horizontal_lines": { "type": "List", "desc": "list of y-values to draw horizontal line", "default": [1.], "kinds": ["1dratio"], },
            "ratio_chi2prob": { "type": "Boolean", "desc": "show chi2 probability for ratio", "default": False, "kinds": ["1dratio"], },
            "ratio_pull": { "type": "Boolean", "desc": "show pulls instead of ratios in ratio pad", "default": False, "kinds": ["1dratio"], },
            "ratio_pull_numbers": { "type": "Boolean", "desc": "show numbers for pulls, and mean/sigma", "default": False, "kinds": ["1dratio"], },
            "ratio_ndivisions": { "type": "Int", "desc": "SetNdivisions integer for ratio", "default": 510, "kinds": ["1dratio"], },
            "ratio_numden_indices": { "type": "List", "desc": "Pair of numerator and denominator histogram indices (from `bgs`) for ratio", "default": None, "kinds": ["1dratio"], },
            "ratio_binomial_errors": { "type": "Boolean", "desc": "Use binomial error propagation when computing ratio eror bars", "default": False, "kinds": ["1dratio"], },
            "ratio_tick_length_scale": { "type": "Float", "desc": "Tick length scale of ratio pads", "default": 1.0, "kinds": ["1dratio"], },

            # Overall
            "title": { "type": "String", "desc": "plot title", "default": "", "kinds": ["1dratio","graph","2d"], },
            "draw_points": { "type": "Boolean", "desc": "draw points instead of fill", "default": False, "kinds": ["1d","1dratio"], },
            "draw_option_2d": { "type": "String", "desc": "hist draw option", "default": "colz", "kinds": ["2d"], },
            "bkg_err_fill_style": { "type": "Int", "desc": "Error shade draw style", "default": 3345, "kinds": ["1d", "1dratio"], },
            "bkg_err_fill_color": { "type": "Int", "desc": "Error shade color", "default": None, "kinds": ["1d", "1dratio"], },
            "ratio_err_fill_style": { "type": "Int", "desc": "Error shade draw style", "default": 3345, "kinds": ["1d", "1dratio"], },
            "ratio_err_fill_color": { "type": "Int", "desc": "Error shade color", "default": None, "kinds": ["1d", "1dratio"], },

            # CMS things
            "cms_label": {"type": "String", "desc": "E.g., 'Preliminary'; default hides label", "default": "Preliminary", "kinds": ["1dratio","graph","2d"]},
            "lumi_value": {"type": "String", "desc": "E.g., 35.9; default hides lumi label", "default": "137", "kinds": ["1dratio","graph","2d"]},
            "lumi_unit": {"type": "String", "desc": "Unit for lumi label", "default": "fb", "kinds": ["1dratio","graph","2d"]},

            # Misc
            "stack_sig": { "type": "Boolean", "desc": "stack signals", "default": True, "kinds": ["1dratio"], },
            "do_stack": { "type": "Boolean", "desc": "stack histograms", "default": True, "kinds": ["1dratio"], },
            "palette_name": { "type": "String", "desc": "color palette: 'default', 'rainbow', 'susy', etc.", "default": "default", "kinds": ["2d"], },
            "show_bkg_errors": { "type": "Boolean", "desc": "show error bar for background stack", "default": False, "kinds": ["1dratio"], },
            "show_bkg_smooth": { "type": "Boolean", "desc": "show smoothed background stack", "default": False, "kinds": ["1dratio"], },
            "bkg_sort_method": { "type": "Boolean", "desc": "how to sort background stack using integrals: 'unsorted', 'ascending', or 'descending'", "default": 'ascending', "kinds": ["1dratio"], },
            "no_ratio": { "type": "Boolean", "desc": "do not draw ratio plot", "default": False, "kinds": ["1dratio"], },

            "max_digits": { "type": "Int", "desc": "integer for max digits", "default": 5, "kinds" : ["1dratio", "graph", "2d"], },


            "bin_text_size": { "type": "Float", "desc": "size of text in bins (TH2::SetMarkerSize)", "default": 1.7, "kinds": ["2d"], },
            "bin_text_format": { "type": "String", "desc": "format string for text in TH2 bins", "default": ".1f", "kinds": ["2d"], },
            "bin_text_smart": { "type": "Boolean", "desc": "change bin text color for aesthetics", "default": False, "kinds": ["2d"], },
            "bin_text_format_smart": { "type": "String", "desc": "python-syntax format string for smart text in TH2 bins taking value and bin error", "default": "{0:.0f}#pm{1:.0f}", "kinds": ["2d"], },

            "hist_line_none": { "type": "Boolean", "desc": "No lines for histograms, only fill", "default": False, "kinds": ["1dratio"], },
            "hist_line_black": { "type": "Boolean", "desc": "Black lines for histograms", "default": False, "kinds": ["1dratio"], },
            "hist_disable_xerrors": { "type": "Boolean", "desc": "Disable the x-error bars on data for 1D hists", "default": True, "kinds": ["1dratio"], },

            "extra_text": { "type": "List", "desc": "list of strings for textboxes", "default": [], "kinds": [ "1dratio","graph"], },
            "extra_text_size": { "type": "Float", "desc": "size for extra text", "default": 0.03, "kinds": [ "1dratio","graph"], },
            "extra_text_xpos": { "type": "Float", "desc": "NDC x position (0 to 1) for extra text", "default": 0.19, "kinds": [ "1dratio","graph"], },
            "extra_text_ypos": { "type": "Float", "desc": "NDC y position (0 to 1) for extra text", "default": 0.79, "kinds": [ "1dratio","graph"], },

            "extra_lines": { "type": "List", "desc": "list of upto 7-tuples (x1,y1,x2,y2,style,width,color) for lines", "default": [], "kinds": [ "1dratio","graph"], },

            "no_overflow": {"type":"Boolean","desc":"Do not plot overflow bins","default": False, "kinds" : ["1dratio"],},

            # Fun
            "us_flag": { "type": "Boolean", "desc": "show the US flag in the corner", "default": False, "kinds": ["1dratio","graph","2d"], },
            "us_flag_coordinates": { "type": "List", "desc": "Specify flag location with (x pos, y pos, size)", "default": [0.68,0.96,0.06], "kinds": ["1dratio","graph","2d"], },

            # Output
            "output_name": { "type": "String", "desc": "output file name/path", "default": "plot.pdf", "kinds": ["1dratio","graph","2d"], },
            "output_ic": { "type": "Boolean", "desc": "run `ic` (imgcat) on output", "default": False, "kinds": ["1dratio","graph","2d"], },
            "output_jsroot": { "type": "Boolean", "desc": "output .json for jsroot", "default": False, "kinds": ["1dratio","graph","2d"], },
            "output_diff_previous": { "type": "Boolean", "desc": "diff the new output file with the previous", "default": False, "kinds": ["1dratio","graph","2d"], },

        }

        self.check_options()

    def usage(self):

        for key,obj in sorted(self.recognized_options.items()):
            default = obj["default"]
            desc = obj["desc"]
            typ = obj["type"]
            kinds = obj["kinds"]
            if self.kind and self.kind not in kinds: continue
            if type(default) is str: default = '"{}"'.format(default)
            print("* `{}` [{}]\n    {} (default: {})".format(key,typ,desc,default))

    def check_options(self):
        for name,val in self.options.items():
            if name not in self.recognized_options:
                print(">>> Option {} not in list of recognized options".format(name))
            else:
                obj = self.recognized_options[name]
                if self.kind not in obj["kinds"]:
                    print(">>> Option {} isn't declared to work with plot type of '{}'".format(name, self.kind))
                else:
                    pass
                    # print ">>> Carry on mate ... {} is fine".format(name)

    def __getitem__(self, key):
        if key in self.options:
            return self.options[key]
        else:
            if key in self.recognized_options:
                return self.recognized_options[key]["default"]
            else:
                print(">>> Hmm, can't find {} anywhere. Typo or intentional?".format(key))
                return None

    def get(self, key, default=None):
        val = self.__getitem__(key)
        if not val: return default
        else: return val

    def is_default(self, key):
        """
        returns True if user has not overriden this particular option
        """
        default = None
        if key in self.recognized_options:
            default = self.recognized_options[key]["default"]
        return (self.__getitem__(key) == default)

    def __setitem__(self, key, value):
        self.options[key] = value

    def __repr__(self):
        return str(self.options)

    def __contains__(self, key):
        return key in self.options

    def __add__(self, other):
        new_opts = {}
        new_opts.update(self.options)
        if type(other) is dict:
            new_opts.update(other)
        else:
            new_opts.update(other.options)
        return Options(new_opts,kind=self.kind)


def overflow(hist):
	return hist

def draw_cms_lumi(c1, nudge, opts ):#, _persist=[]):

	c1.cd()
	t = ROOT.TLatex()
	t.SetTextAlign(11) # align bottom left corner of text
	t.SetTextColor(ROOT.kBlack)
	t.SetTextSize(0.04)
	# get top left corner of current pad, and nudge up the y coord a bit
	xcms  = ROOT.gPad.GetX1() + opts["canvas_main_leftmargin"]
	ycms  = ROOT.gPad.GetY2() - opts["canvas_main_topmargin"] + nudge
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

def draw_extra_stuff(c1, opts):

    if opts["extra_text"]:
        t = ROOT.TLatex()
        t.SetNDC()
        t.SetTextAlign(12)
        t.SetTextFont(42)
        t.SetTextColor(ROOT.kBlack)
        # t.SetTextSize(0.04)
        t.SetTextSize(opts["extra_text_size"])
        for itext, text in enumerate(opts["extra_text"].split(",")):
            t.DrawLatex(opts["extra_text_xpos"],opts["extra_text_ypos"]-itext*5./4*t.GetTextSize(),text)


def get_legend(opts):
    x1,y1,x2,y2 = opts["legend_coordinates"]
    legend_alignment = opts["legend_alignment"]
    height = 0.2
    width = 0.3
    if "bottom" in legend_alignment: y1, y2 = 0.18, 0.18+height
    if "top" 	in legend_alignment: y1, y2 = 0.67, 0.67+height
    if "left" 	in legend_alignment: x1, x2 = 0.18, 0.18+width
    if "right" 	in legend_alignment: x1, x2 = 0.63, 0.63+width
    if "middle" in legend_alignment: x1, x2 = 0.30, 0.30+width

    # scale width and height of legend keeping the sides
    # closest to the plot edges the same (so we expand/contact the legend inwards)
    scalex = opts["legend_scalex"]
    scaley = opts["legend_scaley"]
    toshift_x = (1.-scalex)*(x2-x1)
    toshift_y = (1.-scaley)*(y2-y1)
    if 0.5*(x1+x2) > 0.5: # second half, so keep the right side stationary
        x1 += toshift_x
    else: # keep left side pinned
        x2 -= toshift_x
    if 0.5*(y1+y2) > 0.5: # upper half, so keep the upper side stationary
        y1 += toshift_y
    else: # keep bottom side pinned
        y2 -= toshift_y

    legend = ROOT.TLegend(x1,y1,x2,y2)


    if opts["legend_opacity"] == 1:
        legend.SetFillStyle(0)
    else:
        legend.SetFillColorAlpha(ROOT.kWhite,1.0-opts["legend_opacity"])
    if opts["legend_border"]:
        legend.SetBorderSize(1)
    else:
        legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetNColumns(opts["legend_ncolumns"])
    if opts["legend_column_separation"]: legend.SetColumnSeparation(opts["legend_column_separation"])
    return legend

def do_style_ratio(ratio, opts, tpad):
    #if opts["ratio_range"][1] <= opts["ratio_range"][0]:
    #    # if high <= low, compute range automatically (+-3 sigma interval)
    #    mean, sigma, vals = utils.get_mean_sigma_1d_yvals(ratio)
    #    low = max(mean-3*sigma,min(vals))-sigma/1e3
    #    high = min(mean+3*sigma,max(vals))+sigma/1e3
    #    opts["ratio_range"] = [low,high]
    ratio.SetMarkerStyle(20)
    ratio.SetMarkerSize(1.0)
    ratio.SetLineWidth(2)
    ratio.SetTitle("")
    
    if opts["xaxis_log"]:
        tpad.SetLogx(1)
        ratio.GetXaxis().SetMoreLogLabels(opts["xaxis_moreloglabels"])
        ratio.GetXaxis().SetNoExponent(opts["xaxis_noexponents"])

    ratio.GetYaxis().SetTitle(opts["ratio_name"])
    if opts["ratio_name_size"]  : ratio.GetYaxis().SetTitleSize(opts["ratio_name_size"])
    if opts["ratio_label_size"] : ratio.GetYaxis().SetLabelSize(opts["ratio_label_size"])
    if opts["ratio_yaxis_title_offset"]: ratio.GetYaxis().SetTitleOffset(opts["ratio_yaxis_title_offset"])
    if opts["ratio_yaxis_label_offset"]: ratio.GetYaxis().SetLabelOffset(opts["ratio_yaxis_label_offset"])
    ratio.GetYaxis().SetRangeUser(*opts["ratio_range"])
    ratio.GetYaxis().SetNdivisions(505)


    if opts["xaxis_label"]: ratio.GetXaxis().SetTitle(opts["xaxis_label"])
    if opts["xaxis_range"]: ratio.GetXaxis().SetRangeUser(*opts["xaxis_range"])

    if opts["ratio_name_size"]  : ratio.GetXaxis().SetTitleSize(opts["ratio_name_size"])
    if opts["ratio_ndivisions"] : ratio.GetXaxis().SetNdivisions(opts["ratio_ndivisions"])
    if opts["ratio_label_size"] : ratio.GetXaxis().SetLabelSize(opts["ratio_label_size"])   
    if opts["xaxis_bin_text_labels"]: ratio.GetXaxis().SetLabelSize(0.18)

    if opts["ratio_xaxis_title_offset"]: ratio.GetXaxis().SetTitleOffset(opts["ratio_xaxis_title_offset"])
    if opts["ratio_xaxis_label_offset"]: ratio.GetXaxis().SetLabelOffset(opts["ratio_xaxis_label_offset"])
    ratio.GetXaxis().SetTickSize(0.06 * opts["ratio_tick_length_scale"])
    ratio.GetYaxis().SetTickSize(0.03 * opts["ratio_tick_length_scale"])
    return 

def save(c1, opts):

    fname = opts["output_name"]
    dirname = os.path.dirname(fname)
    if dirname and not os.path.isdir(dirname):
        print(">>> Plot should go inside {}/, but it doesn't exist.".format(dirname))
        print(">>> Instead of crashing, I'll do you a solid and make it".format(dirname))
        os.system("mkdir -p {}".format(dirname))

    orig_fname = None
    if opts["output_diff_previous"]:
        if os.path.exists(fname):
            orig_fname = fname.replace(".pdf","_orig.pdf")
            #orig_fname = fname.replace(".pdf","_orig.pdf")
            os.system("mv {} {}".format(fname, orig_fname))

    print(">>> Saving {}".format(fname))
    c1.SaveAs(fname)

    if opts["output_diff_previous"]:
        fname_diff = "diff.png"
        utils.diff_images(orig_fname,fname, output=fname_diff)
        os.system("ic {}".format(fname_diff))
        if orig_fname:
            os.system("rm {}".format(orig_fname))

    if opts["output_ic"]:
        os.system("ic {}".format(fname))
    if opts["output_jsroot"]:
        r.TBufferJSON.ExportToFile("{}.json".format(fname.rsplit(".",1)[0]),c1)

    return

def getMultipleSRHisto(fname,srs,selname,dist):

	froot = ROOT.TFile.Open(fname)

	# get hist from all SRs
	hists = []
	for sr in srs: 
		histname = "{}__{}".format(sr,dist)
		hist = froot.Get(histname)	
		hists.append(hist)

	hist_merged = hists[0].Clone()
	hist_merged.Reset()
	for hist in hists:
		hist_merged.Add(hist)
	
 
	if "data.root"  in fname : hist_merged.SetName( selname + "__" + dist + "_data"   )
	elif "photon"   in fname : hist_merged.SetName( selname + "__" + dist + "_photon" )
	elif "qflip"    in fname : hist_merged.SetName( selname + "__" + dist + "_qflip"  ) 
	elif "fakes"    in fname : hist_merged.SetName( selname + "__" + dist + "_fakes"  ) 
	elif "lostlep"  in fname : hist_merged.SetName( selname + "__" + dist + "_lostlep") 
	elif "prompt"   in fname : hist_merged.SetName( selname + "__" + dist + "_prompt" ) 
	elif "www"      in fname : hist_merged.SetName( selname + "__" + dist + "_WWW"    ) 
	elif "wwz"      in fname : hist_merged.SetName( selname + "__" + dist + "_WWZ"    ) 
	elif "wzz"      in fname : hist_merged.SetName( selname + "__" + dist + "_WZZ"    ) 
	elif "zzz"      in fname : hist_merged.SetName( selname + "__" + dist + "_ZZZ"    ) 
	elif "vvv.root" in fname : hist_merged.SetName( selname + "__" + dist + "_VVV"    ) 
	elif "nonzz"    in fname : hist_merged.SetName( selname + "__" + dist + "_nonzz"  ) 
	elif "zz"       in fname : hist_merged.SetName( selname + "__" + dist + "_zz"     ) 
	elif "ttz"      in fname : hist_merged.SetName( selname + "__" + dist + "_ttz"    ) 
	elif "twz"      in fname : hist_merged.SetName( selname + "__" + dist + "_twz"    ) 
	elif "wz"       in fname : hist_merged.SetName( selname + "__" + dist + "_wz"     ) 
	elif "other"    in fname : hist_merged.SetName( selname + "__" + dist + "_other"  ) 

	hist_merged.SetDirectory(0)
	return hist_merged

def getMultipleSRHistos(fnames,srs,selname,dist):
	hists = []
	for fname in fnames:
		hists.append(getMultipleSRHisto(fname,srs,selname,dist))
	return hists

def getHisto(fname,histname):

	#print(fname,histname)

	froot = ROOT.TFile.Open(fname)
	hist = froot.Get(histname)	
	hist.SetDirectory(0)

	if "data"    in fname : hist.SetName( hist.GetName() + "_data"   )
	if "photon"  in fname : hist.SetName( hist.GetName() + "_photon" )
	if "qflip"   in fname : hist.SetName( hist.GetName() + "_qflip"  ) 
	if "fakes"   in fname : hist.SetName( hist.GetName() + "_fakes"  ) 
	if "lostlep" in fname : hist.SetName( hist.GetName() + "_lostlep") 
	if "prompt"  in fname : hist.SetName( hist.GetName() + "_prompt" ) 
	if "www"     in fname : hist.SetName( hist.GetName() + "_WWW"    ) 
	if "wwz"     in fname : hist.SetName( hist.GetName() + "_WWZ"    ) 
	if "wzz"     in fname : hist.SetName( hist.GetName() + "_WZZ"    ) 
	if "zzz"     in fname : hist.SetName( hist.GetName() + "_ZZZ"    ) 
	if "vvv"     in fname : hist.SetName( hist.GetName() + "_VVV"    )
	return hist

def getHistos(fnames,histname):
	hists = []
	for fname in fnames:
		hists.append(getHisto(fname,histname))
	return hists


def get_stack_maximum(data, stack, opts={}):
    scalefact = 1.05
    if opts["yaxis_range"]:
        return opts["yaxis_range"][1]
    if data:
        return scalefact*max(data.GetMaximum(),stack.GetMaximum())
    else:
        return scalefact*stack.GetMaximum()

def data_style(hist,opts):
	hist.SetMarkerStyle(20)
	hist.SetMarkerColor(ROOT.kBlack)
	hist.SetLineWidth(2)
	hist.SetMarkerSize(1.0)
	hist.SetLineColor(ROOT.kBlack)

	if opts["nbins"]: 
		bins_now = hist.GetNbinsX() 
		rebin_fact = int(bins_now/(opts["nbins"]))
		hist.Rebin(rebin_fact)
	if opts["xaxis_bins"]:
		nbins = len(opts["xaxis_bins"])-1
		hist =hist.Rebin( nbins,hist.GetName()+"_", array("d",opts["xaxis_bins"]) )
	if opts["xaxis_bin_text_labels"]:
		for i in range(len( opts["xaxis_bin_text_labels"])):
			hist.GetXaxis().SetBinLabel(i+1,opts["xaxis_bin_text_labels"][i])

	return hist

def background_style(hist,opts):
	name = hist.GetName()
	col = ROOT.kBlack

	if "BDT_lostlep_prompt_SS2J" in name: name = name.replace("BDT_lostlep_prompt_SS2J","")
	if "BDT_lostlep_prompt_SS1J" in name: name = name.replace("BDT_lostlep_prompt_SS1J","")
	if "BDT_lostlep_prompt_SFOS" in name: name = name.replace("BDT_lostlep_prompt_SFOS","")
	if "BDT_photon_fakes_SS1J"   in name: name = name.replace("BDT_photon_fakes_SS1J","")
	if "BDT_photon_fakes_SS2J"   in name: name = name.replace("BDT_photon_fakes_SS2J","")
	if "BDT_photon_fakes_SFOS"   in name: name = name.replace("BDT_photon_fakes_SFOS","")

	if "photon"    in name : col = 920 
	elif "qflip"   in name : col = 2007 
	elif "fakes"   in name : col = 2005 
	elif "lostlep" in name : col = 2003 
	elif "prompt"  in name : col = 2001 
	elif "nonzz"   in name : col = 920
	elif "zz"      in name : col = 4020 
	elif "ttz"     in name : col = 4305 
	elif "twz"     in name : col = 4024 
	elif "wz"      in name : col = 7013
	elif "other"   in name : col = 920

	if opts["nbins"]: 
		bins_now = hist.GetNbinsX() 
		rebin_fact = int(bins_now/(opts["nbins"]))
		#print("REBIN {}".format(rebin_fact))
		hist.Rebin(rebin_fact)
	if opts["xaxis_bins"]:
		nbins = len(opts["xaxis_bins"])-1
		hist =hist.Rebin( nbins,hist.GetName()+"_", array("d",opts["xaxis_bins"]) )
	if opts["xaxis_bin_text_labels"]:
		for i in range(len( opts["xaxis_bin_text_labels"])):
			hist.GetXaxis().SetBinLabel(i+1,opts["xaxis_bin_text_labels"][i])
		hist.GetXaxis().SetLabelSize(0.07)
	if opts["yaxis_label"]: hist.GetYaxis().SetTitle(opts["yaxis_label"])

	#hist.GetYaxis().SetTitleOffset(0.5)
	#hist.GetYaxis().SetTitleSize(0.05)

	#hist.SetLineColor(col)
	hist.SetLineColor(ROOT.kBlack)
	hist.SetMarkerColor(col)
	hist.SetMarkerSize(0)
	hist.SetFillColorAlpha(col,0.8) # may want option for this

	if opts["yaxis_ndivisions"]: hist.GetYaxis().SetNdivisions(opts["yaxis_ndivisions"])
	if opts["xaxis_ndivisions"]: hist.GetXaxis().SetNdivisions(opts["xaxis_ndivisions"])

	return hist

def signal_style(hist,opts):
	name = hist.GetName()
	#print(name)
	col = ROOT.kBlack
	if "VVV" in name : col = ROOT.kRed 
	if "WWW" in name : col = ROOT.kRed 
	if "WWZ" in name : col = ROOT.kBlue 
	if "WZZ" in name : col = ROOT.kOrange-4 
	if "ZZZ" in name : col = ROOT.kTeal-5 

	#print(name,col)
	
	if opts["stack_sig"]:
		hist.SetLineColor(ROOT.kBlack)
		hist.SetMarkerColor(col)
		hist.SetMarkerSize(0)
		hist.SetFillColorAlpha(col,1.0) # may want option for this
	else : 
		hist.SetMarkerStyle(1) # 2 has errors
		hist.SetMarkerColor(col)
		hist.SetLineWidth(4)
		hist.SetMarkerSize(0.8)
		hist.SetLineColor(col)
		hist.SetFillColorAlpha(col,0.0) # may want option for this

		if opts["signal_scale"]:
			hist.Scale(opts["signal_scale"])

	if opts["nbins"]: 
		bins_now = hist.GetNbinsX() 
		rebin_fact = int(bins_now/(opts["nbins"]))
		hist.Rebin(rebin_fact)
	if opts["xaxis_bins"]:
		nbins = len(opts["xaxis_bins"])-1
		hist =hist.Rebin( nbins,hist.GetName()+"_", array("d",opts["xaxis_bins"]) )
	if opts["xaxis_bin_text_labels"]:
		for i in range(len( opts["xaxis_bin_text_labels"])):
			hist.GetXaxis().SetBinLabel(i+1,opts["xaxis_bin_text_labels"][i])

	return hist


# Color schemes from Hannsjoerg for WWW analysis
mycolors = []
mycolors.append(ROOT.TColor(2001 , 91  / 255. , 187 / 255. , 241 / 255.)) #light-blue
mycolors.append(ROOT.TColor(2002 , 60  / 255. , 144 / 255. , 196 / 255.)) #blue
mycolors.append(ROOT.TColor(2003 , 230 / 255. , 159 / 255. , 0   / 255.)) #orange
mycolors.append(ROOT.TColor(2004 , 180 / 255. , 117 / 255. , 0   / 255.)) #brown
mycolors.append(ROOT.TColor(2005 , 245 / 255. , 236 / 255. , 69  / 255.)) #yellow
mycolors.append(ROOT.TColor(2006 , 215 / 255. , 200 / 255. , 0   / 255.)) #dark yellow
mycolors.append(ROOT.TColor(2007 , 70  / 255. , 109 / 255. , 171 / 255.)) #blue-violet
mycolors.append(ROOT.TColor(2008 , 70  / 255. , 90  / 255. , 134 / 255.)) #violet
mycolors.append(ROOT.TColor(2009 , 55  / 255. , 65  / 255. , 100 / 255.)) #dark violet
mycolors.append(ROOT.TColor(2010 , 120 / 255. , 160 / 255. , 0   / 255.)) #light green
mycolors.append(ROOT.TColor(2011 , 0   / 255. , 158 / 255. , 115 / 255.)) #green
mycolors.append(ROOT.TColor(2012 , 204 / 255. , 121 / 255. , 167 / 255.)) #pink?

mycolors.append(ROOT.TColor(4001 , 49  / 255. , 76  / 255. , 26  / 255. ))
mycolors.append(ROOT.TColor(4002 , 33  / 255. , 164 / 255. , 105  / 255. ))
mycolors.append(ROOT.TColor(4003 , 176 / 255. , 224 / 255. , 160 / 255. ))
mycolors.append(ROOT.TColor(4004 , 210 / 255. , 245 / 255. , 200 / 255. ))
mycolors.append(ROOT.TColor(4005 , 232 / 255. , 249 / 255. , 223 / 255. ))
mycolors.append(ROOT.TColor(4006 , 253 / 255. , 156 / 255. , 207 / 255. ))
mycolors.append(ROOT.TColor(4007 , 121 / 255. , 204 / 255. , 158 / 255. ))
mycolors.append(ROOT.TColor(4008 , 158 / 255. ,   0 / 255. ,  42 / 255. ))
mycolors.append(ROOT.TColor(4009 , 176 / 255. ,   0 / 255. , 195 / 255. ))
mycolors.append(ROOT.TColor(4010 ,  20 / 255. , 195 / 255. ,   0 / 255. ))
mycolors.append(ROOT.TColor(4011 , 145 / 255. ,   2 / 255. , 206 / 255. ))
mycolors.append(ROOT.TColor(4012 , 255 / 255. ,   0 / 255. , 255 / 255. ))
mycolors.append(ROOT.TColor(4013 , 243 / 255. ,  85 / 255. ,   0 / 255. ))
mycolors.append(ROOT.TColor(4014 , 157 / 255. , 243 / 255. , 130 / 255. ))
mycolors.append(ROOT.TColor(4015 , 235 / 255. , 117 / 255. , 249 / 255. ))
mycolors.append(ROOT.TColor(4016 ,  90 / 255. , 211 / 255. , 221 / 255. ))
mycolors.append(ROOT.TColor(4017 ,  85 / 255. , 181 / 255. ,  92 / 255. ))
mycolors.append(ROOT.TColor(4018 , 172 / 255. ,  50 / 255. ,  60 / 255. ))
mycolors.append(ROOT.TColor(4019 ,  42 / 255. , 111 / 255. , 130 / 255. ))

mycolors.append(ROOT.TColor(4020 , 240 / 255. , 155 / 255. , 205 / 255. )) # ATLAS pink
mycolors.append(ROOT.TColor(4021 ,  77 / 255. , 161 / 255. ,  60 / 255. )) # ATLAS green
mycolors.append(ROOT.TColor(4022 ,  87 / 255. , 161 / 255. , 247 / 255. )) # ATLAS blue
mycolors.append(ROOT.TColor(4023 , 196 / 255. , 139 / 255. , 253 / 255. )) # ATLAS darkpink
mycolors.append(ROOT.TColor(4024 , 205 / 255. , 240 / 255. , 155 / 255. )) # Complementary

mycolors.append(ROOT.TColor(4101 , 102 / 255. , 102 / 255. , 204 / 255. )) # ATLAS HWW / WW
mycolors.append(ROOT.TColor(4102 ,  89 / 255. , 185 / 255. ,  26 / 255. )) # ATLAS HWW / DY
mycolors.append(ROOT.TColor(4103 , 225 / 255. ,  91 / 255. , 226 / 255. )) # ATLAS HWW / VV
mycolors.append(ROOT.TColor(4104 , 103 / 255. , 236 / 255. , 235 / 255. )) # ATLAS HWW / misid

mycolors.append(ROOT.TColor(4201 ,  16 / 255. , 220 / 255. , 138 / 255. )) # Signal complementary

mycolors.append(ROOT.TColor(4305 ,   0/255. , 208/255. , 145/255.)) # green made up
mycolors.append(ROOT.TColor(7013 , 163/255. , 155/255. ,  47/255.)) #alt y

default_colors = []
default_colors.append(2005)
default_colors.append(2001)
default_colors.append(2003)
default_colors.append(2007)
default_colors.append(920)
default_colors.extend(range(2001, 2013))
default_colors.extend(range(7001, 7018))
