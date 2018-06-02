"""
.. module:: VisPlotly
    :platform: Unix, Windows
    :synopsis: Plotly visualization component for NURBS-Python (experimental)

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

from . import Abstract
from . import utilities

from . import numpy as np
import plotly
from plotly import graph_objs


class VisConfig(Abstract.VisConfigAbstract):
    """ Configuration class for Plotly visualization module.

    This class is only required when you prefer to change the default plotting behavior, such as hiding control points
    plot or legend. By default, the following variables and their default values are used in all ``VisPlotly``
    visualization classes.

    * ``ctrlpts`` (True or False, *default: True*): Enables/Disables control points polygon/grid plot on the figure
    * ``legend`` (True or False): Enables/Disables legend on the figure
    * ``axes`` (True or False): Enables/Disables axes and grid on the figure
    * ``figure_size`` (list, *default: [800, 800]*): Size of the figure in (x, y)
    * ``linewidth`` (int, *default: 2*): thickness of the lines on the figure

    The following example illustrates the usage of the configuration class.

    .. code-block:: python

        # Create a surface (or a curve) instance
        surf = NURBS.Surface()

        # Skipping degree, knot vector and control points assignments

        # Create a visualization configuration instance with no legend, no axes and no control points grid
        vis_config = VisPlotly.VisConfig(legend=False, axes=False, ctrlpts=False)

        # Create a visualization method instance using the configuration above
        vis_obj = VisPlotly.VisSurface(vis_config)

        # Set the visualization method of the surface object
        surf.vis = vis_obj

        # Plot the surface
        surf.render()

    Please refer to the **Examples Repository** for more details.
    """
    def __init__(self, **kwargs):
        super(VisConfig, self).__init__(**kwargs)
        self.display_ctrlpts = kwargs.get('ctrlpts', True)
        self.figure_size = kwargs.get('figure_size', [800, 800])
        self.display_legend = kwargs.get('legend', True)
        self.display_axes = kwargs.get('axes', True)
        self.line_width = kwargs.get('linewidth', 2)


class VisCurve2D(Abstract.VisAbstract):
    """ Plotly visualization module for 2D Curves """
    def __init__(self, config=VisConfig()):
        super(VisCurve2D, self).__init__(config=config)

    def render(self):
        """ Plots the curve and the control points polygon """
        if not self._plots:
            return

        plot_data = []
        for plot in self._plots:
            pts = np.array(plot['ptsarr'])

            # Plot control points
            if plot['type'] == 'ctrlpts' and self._config.display_ctrlpts:
                figure = graph_objs.Scatter(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    name=plot['name'],
                    mode='lines+markers',
                    line=dict(
                        color=plot['color'],
                        width=self._config.line_width,
                        dash='dashdot'
                    )
                )
                plot_data.append(figure)

            # Plot evaluated points
            if plot['type'] == 'evalpts':
                figure = graph_objs.Scatter(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    name=plot['name'],
                    mode='lines',
                    line=dict(
                        color=plot['color'],
                        width=self._config.line_width
                    )
                )
                plot_data.append(figure)

        plot_layout = dict(
            width=self._config.figure_size[0],
            height=self._config.figure_size[1],
            autosize=False,
            showlegend=self._config.display_legend,
            yaxis=dict(
                scaleanchor="x",
                showgrid=self._config.display_axes,
                showline=self._config.display_axes,
                zeroline=self._config.display_axes,
                showticklabels=self._config.display_axes,
            ),
            xaxis=dict(
                showgrid=self._config.display_axes,
                showline=self._config.display_axes,
                zeroline=self._config.display_axes,
                showticklabels=self._config.display_axes,
            )
        )

        plotly.offline.plot({
            "data": plot_data,
            "layout": plot_layout
        }, show_link=False)


class VisCurve3D(Abstract.VisAbstract):
    """ Plotly visualization module for 3D Curves """
    def __init__(self, config=VisConfig()):
        super(VisCurve3D, self).__init__(config=config)

    def render(self):
        """ Plots the curve and the control points polygon """
        if not self._plots:
            return

        plot_data = []
        for plot in self._plots:
            pts = np.array(plot['ptsarr'])

            # Plot control points
            if plot['type'] == 'ctrlpts' and self._config.display_ctrlpts:
                figure = graph_objs.Scatter3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=pts[:, 2],
                    name=plot['name'],
                    mode='lines+markers',
                    line=dict(
                        color=plot['color'],
                        width=self._config.line_width,
                        dash='dashdot'
                    ),
                    marker=dict(
                        color=plot['color'],
                        size=self._config.line_width
                    )
                )
                plot_data.append(figure)

            # Plot evaluated points
            if plot['type'] == 'evalpts':
                figure = graph_objs.Scatter3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=pts[:, 2],
                    name=plot['name'],
                    mode='lines',
                    line=dict(
                        color=plot['color'],
                        width=self._config.line_width
                    ),
                )
                plot_data.append(figure)

        plot_layout = dict(
            width=self._config.figure_size[0],
            height=self._config.figure_size[1],
            autosize=False,
            showlegend=self._config.display_legend,
            scene=graph_objs.Scene(
                xaxis=graph_objs.XAxis(
                    showgrid=self._config.display_axes,
                    showline=self._config.display_axes,
                    zeroline=self._config.display_axes,
                    showticklabels=self._config.display_axes,
                    title='',
                ),
                yaxis=graph_objs.YAxis(
                    showgrid=self._config.display_axes,
                    showline=self._config.display_axes,
                    zeroline=self._config.display_axes,
                    showticklabels=self._config.display_axes,
                    title='',
                ),
                zaxis=graph_objs.ZAxis(
                    showgrid=self._config.display_axes,
                    showline=self._config.display_axes,
                    zeroline=self._config.display_axes,
                    showticklabels=self._config.display_axes,
                    title='',
                ),
            ),
        )

        plotly.offline.plot({
            "data": plot_data,
            "layout": plot_layout
        }, show_link=False)


class VisSurface(Abstract.VisAbstractSurf):
    """ Plotly visualization module for Surfaces """
    def __init__(self, config=VisConfig()):
        super(VisSurface, self).__init__(config=config)

    def render(self):
        """ Plots the surface and the control points grid """
        if not self._plots:
            return

        plot_data = []
        for plot in self._plots:
            # Plot control points
            if plot['type'] == 'ctrlpts' and self._config.display_ctrlpts:
                pts = np.array(utilities.make_quad(plot['ptsarr'], plot['size'][1], plot['size'][0]))
                cp_z = pts[:, 2] + self._ctrlpts_offset
                figure = graph_objs.Scatter3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=cp_z,
                    name=plot['name'],
                    mode='lines+markers',
                    line=dict(
                        color=plot['color'],
                        width=self._config.line_width,
                        dash='solid'
                    ),
                    marker=dict(
                        color=plot['color'],
                        size=self._config.line_width
                    )
                )
                plot_data.append(figure)

            # Plot evaluated points
            if plot['type'] == 'evalpts':
                pts = np.array(utilities.make_triangle(plot['ptsarr'], plot['size'][1], plot['size'][0]))
                figure = graph_objs.Scatter3d(
                    x=pts[:, 0],
                    y=pts[:, 1],
                    z=pts[:, 2],
                    name=plot['name'],
                    mode='lines',
                    line=dict(
                        color=plot['color'],
                        width=self._config.line_width
                    ),
                )
                plot_data.append(figure)

        plot_layout = dict(
            width=self._config.figure_size[0],
            height=self._config.figure_size[1],
            autosize=False,
            showlegend=self._config.display_legend,
            scene=graph_objs.Scene(
                xaxis=graph_objs.XAxis(
                    showgrid=self._config.display_axes,
                    showline=self._config.display_axes,
                    zeroline=self._config.display_axes,
                    showticklabels=self._config.display_axes,
                    title='',
                ),
                yaxis=graph_objs.YAxis(
                    showgrid=self._config.display_axes,
                    showline=self._config.display_axes,
                    zeroline=self._config.display_axes,
                    showticklabels=self._config.display_axes,
                    title='',
                ),
                zaxis=graph_objs.ZAxis(
                    showgrid=self._config.display_axes,
                    showline=self._config.display_axes,
                    zeroline=self._config.display_axes,
                    showticklabels=self._config.display_axes,
                    title='',
                ),
            ),
        )

        plotly.offline.plot({
            "data": plot_data,
            "layout": plot_layout
        }, show_link=False)