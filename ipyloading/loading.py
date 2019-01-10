# coding=utf-8
""" Loading widgets for the Jupyter Notebook or Labs.
Main resource: https://loading.io/css/ """

from ipywidgets import HTML
from string import Template
from traitlets import Unicode, Int, Float, observe
from uuid import uuid4


class Loading(HTML):
    """ Open source CSS Loading animations from https://loading.io/css/

    This is the base Class.

    It uses `string.Template` for templates
    (https://docs.python.org/3.5/library/string.html)

    It has 3 main parameters: `size`, `color`, and `background_color`. You can
    add custom parameters in the subclass implementation.

    A simple example would be:

    .. code:: python

        css = \"""
        .customclass {
            color: ${color};
        }
        \"""

    It has three methods that can be overwritten by the subclasses in order to
    implement custom css properties: `compute_size`, `compute_color` and
    `compute_background_color`. This methods must return a `dict` holding the
    'extra' parameters.

    See 'Ring' subclass for an example.
    """
    size = Int()
    border = Float(allow_none=True)
    color = Unicode()
    background_color = Unicode()

    def __init__(self, size=20, color='black', background_color='',
                 border=None, extra={}, css='', html='', **kwargs):
        """

        :param size: size of the widget
        :param color: color of the
        :param background_color:
        :param css: the css code to render
        :param html: the html code to render
        :param kwargs:
        """

        self.css = css
        self.html = html
        self.uid = 'a'+str(uuid4())
        self.extra = extra

        self.template = Template("""
        <head>
          <style>
            ${css}
          </style>
        </head>
        <body>
          <div class="${css_class}">
            ${html}
          </div>
        </body>
        """)

        self.css_params = dict(size=size, color=color, border=border,
                               background_color=background_color,
                               css_class=self.uid, **self.extra)

        super(Loading, self).__init__(**kwargs)
        self.size = size
        self.border = border
        self.color = color
        self.background_color = background_color

        self.render()

    @observe('size')
    def _ob_size(self, change):
        size = change['new']

        params = self.compute_size(size)
        if isinstance(params, dict):
            for key, val in params.items():
                self.css_params[key] = val

        self.render()

    @observe('border')
    def _ob_border(self, change):
        border = change['new']

        params = self.compute_border(border)
        if isinstance(params, dict):
            for key, val in params.items():
                self.css_params[key] = val

        self.render()

    @observe('color')
    def _ob_color(self, change):
        color = change['new']

        params = self.compute_color(color)
        if isinstance(params, dict):
            for key, val in params.items():
                self.css_params[key] = val

        self.render()

    @observe('background_color')
    def _ob_background_color(self, change):
        color = change['new']

        params = self.compute_background_color(color)
        if isinstance(params, dict):
            for key, val in params.items():
                self.css_params[key] = val

        self.render()

    def render(self):
        """ Makes templates substitutions to fill css and html values """
        # Fill CSS params
        css = Template(self.css).safe_substitute(**self.css_params)

        # Fill with unique class id
        html = Template(self.html).safe_substitute(css_class=self.uid)

        # Change HTML value. HTML is observing value so it will automatically
        # change
        self.value = self.template.safe_substitute(
            css=css, html=html, css_class=self.uid)

    def compute_size(self, size):
        return dict(size=size)

    def compute_border(self, border):
        if not border:
            self.border = self.size * 0.1
        else:
            self.border = border

        return dict(border=self.border)

    def compute_color(self, color):
        return dict(color=color)

    def compute_background_color(self, color):
        return dict(background_color=color)


class Ring(Loading):

    def __init__(self, **kwargs):
        css = """
        .${css_class} {
          display: inline-block;
          position: relative;
          width: ${width}px;
          height: ${height}px;
        }
        .${css_class} div {
          box-sizing: border-box;
          display: block;
          position: absolute;
          width: ${inner_width}px;
          height: ${inner_height}px;
          margin: ${margin}px;
          border: ${border}px solid ${color};
          border-radius: 50%;
          animation: ${css_class} 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
          border-color: ${color} transparent transparent transparent;
          background-color: ${background_color};
        }
        .${css_class} div:nth-child(1) {
          animation-delay: -0.45s;
        }
        .${css_class} div:nth-child(2) {
          animation-delay: -0.3s;
        }
        .${css_class} div:nth-child(3) {
          animation-delay: -0.15s;
        }
        @keyframes ${css_class} {
          0% {
            transform: rotate(0deg);
          }
          100% {
            transform: rotate(360deg);
          }
        }
        """
        html = """        
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        """
        self.extra = self.compute_size(self.size)
        super(Ring, self).__init__(css=css, html=html,
                                   extra=self.extra, **kwargs)

    def compute_size(self, size):

        width = size
        height = size
        inner_width = int(size*0.8)
        inner_height = int(size*0.8)
        margin = self.border
        extra = dict(inner_width=inner_width, inner_height=inner_height,
                     margin=margin, width=width, height=height)
        return extra