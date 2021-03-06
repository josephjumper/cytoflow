#!/usr/bin/env python2.7

# (c) Massachusetts Institute of Technology 2015-2016
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
Created on Apr 23, 2015

@author: brian
'''

from traits.api import provides, Callable, Str
from traitsui.api import View, Item, Controller, EnumEditor, VGroup
from envisage.api import Plugin, contributes_to
from pyface.api import ImageResource

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from cytoflow import Histogram2DView
import cytoflow.utility as util

from cytoflowgui.subset_editor import SubsetEditor
from cytoflowgui.ext_enum_editor import ExtendableEnumEditor
from cytoflowgui.color_text_editor import ColorTextEditor
from cytoflowgui.view_plugins.i_view_plugin \
    import IViewPlugin, VIEW_PLUGIN_EXT, ViewHandlerMixin, PluginViewMixin

class Histogram2DHandler(Controller, ViewHandlerMixin):
    '''
    classdocs
    '''

    def default_traits_view(self):
        return View(VGroup(
                    VGroup(Item('name'),
                           Item('xchannel',
                                editor=EnumEditor(name='context.channels'),
                                label = "X Channel"),
                           Item('xscale',
                                label = "X Scale"),
                           Item('ychannel',
                                editor=EnumEditor(name='context.channels'),
                                label = "Y Channel"),
                           Item('yscale',
                                label = "Y Scale"),
                           Item('xfacet',
                                editor=ExtendableEnumEditor(name='context.conditions_names',
                                                            extra_items = {"None" : ""}),
                                label = "Horizontal\nFacet"),
                           Item('yfacet',
                                editor=ExtendableEnumEditor(name='context.conditions_names',
                                                            extra_items = {"None" : ""}),
                                label = "Vertical\nFacet"),
                           Item('huefacet',
                                editor=ExtendableEnumEditor(name='context.conditions_names',
                                                            extra_items = {"None" : ""}),
                                label="Color\nFacet"),
                           Item('plotfacet',
                                editor=ExtendableEnumEditor(name='context.conditions_names',
                                                            extra_items = {"None" : ""}),
                                label = "Tab\nFacet"),
                           label = "2D Histogram",
                           show_border = False),
                    VGroup(Item('subset_dict',
                                show_label = False,
                                editor = SubsetEditor(conditions = "context.conditions")),
                           label = "Subset",
                           show_border = False,
                           show_labels = False),
                    Item('context.view_warning',
                         resizable = True,
                         visible_when = 'context.view_warning',
                         editor = ColorTextEditor(foreground_color = "#000000",
                                                 background_color = "#ffff99")),
                    Item('context.view_error',
                         resizable = True,
                         visible_when = 'context.view_error',
                         editor = ColorTextEditor(foreground_color = "#000000",
                                                  background_color = "#ff9191"))))

class Histogram2DPluginView(PluginViewMixin, Histogram2DView):
    handler_factory = Callable(Histogram2DHandler)
    plotfacet = Str

    def enum_plots_wi(self, wi):
        if not self.plotfacet:
            return iter([])
        
        if self.plotfacet and self.plotfacet not in wi.result.conditions:
            raise util.CytoflowViewError("Plot facet {0} not in the experiment"
                                    .format(self.huefacet))
        values = np.sort(pd.unique(wi.result[self.plotfacet]))
        return iter(values)
    
    def plot_wi(self, wi):
        self.plot(wi.result, wi.current_plot)
    
    def plot(self, experiment, plot_name = None, **kwargs):
        if self.plotfacet and plot_name:
            experiment = experiment.subset(self.plotfacet, plot_name)

        Histogram2DView.plot(self, experiment, **kwargs)
        
        if self.plotfacet and plot_name is not None:
            plt.title("{0} = {1}".format(self.plotfacet, plot_name))

@provides(IViewPlugin)
class Histogram2DPlugin(Plugin):
    """
    classdocs
    """

    id = 'edu.mit.synbio.cytoflowgui.view.histogram2d'
    view_id = 'edu.mit.synbio.cytoflow.view.histogram2d'
    short_name = "2D Histogram"

    def get_view(self):
        return Histogram2DPluginView()
    
    def get_icon(self):
        return ImageResource('histogram_2d')

    @contributes_to(VIEW_PLUGIN_EXT)
    def get_plugin(self):
        return self
        