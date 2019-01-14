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

    _border = None
    _size = None
    _margin = None

    def __init__(self, size=20, color='black', background_color='',
                 border=None, margin=None, extra={}, css='', html='',
                 **kwargs):
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
        self.margin = margin
        self.color = color
        self.background_color = background_color

        self.render()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        # compute new params
        params = self.compute_size(size)

        # modify css params for rendering
        if isinstance(params, dict):
            # iterate over the new params because there could be more than
            # one
            for key, val in params.items():
                self.css_params[key] = val

        # assign new param
        self._size = params['size']

        # render
        self.render()

    @property
    def margin(self):
        return self._margin

    @margin.setter
    def margin(self, margin):
        params = self.compute_margin(margin)
        if isinstance(params, dict):
            for key, val in params.items():
                self.css_params[key] = val

        self._margin = params['margin']
        self.render()

    @property
    def border(self):
        return self._border

    @border.setter
    def border(self, border):
        params = self.compute_border(border)
        if isinstance(params, dict):
            for key, val in params.items():
                self.css_params[key] = val

        self._border = params['border']
        self.render()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        params = self.compute_color(color)
        if isinstance(params, dict):
            for key, val in params.items():
                self.css_params[key] = val

        self._color = params['color']
        self.render()

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, background_color):
        params = self.compute_background_color(background_color)
        if isinstance(params, dict):
            for key, val in params.items():
                self.css_params[key] = val

        self._background_color = params['background_color']
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
        return dict(border=border)

    def compute_margin(self, margin):
        return dict(margin=margin)

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
        # self.extra = self.compute_extra(self.size)
        super(Ring, self).__init__(css=css, html=html, **kwargs)

        # self.extra = self.compute_extra(self.size)

    def compute_size(self, size):

        width = size
        height = size
        inner_width = size * 0.8
        inner_height = size * 0.8
        extra = dict(inner_width=inner_width, inner_height=inner_height,
                     width=width, height=height, size=size)
        return extra

    def compute_border(self, border):

        size = float(self.css_params['inner_height'])

        if not border:
            border = size * 0.1
        else:
            if isinstance(border, (int, float)):
                border = border
            elif isinstance(border, str):
                last = border[-1:]
                last2 = border[-2:]

                if last == '%':
                    number = float(border[:-1])/100
                    border = size * number
                elif last2 == 'px':
                    number = float(border[:-2])
                    border = number

        # trim to 50% if greater
        if border > (size * 0.5):
            border = size * 0.5

        return dict(border=border)

    def compute_margin(self, margin):
        if not margin:
            margin = self.size * 0.1
        else:
            if isinstance(margin, (int, float)):
                margin = margin
            elif isinstance(margin, str):
                margin = int(margin)

        if margin > (self.size * 0.1):
            print('margin overfitted')
            inner = float(self.css_params['inner_height'])
            self.size = inner + 2*margin

        return dict(margin=margin)