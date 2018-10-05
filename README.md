## Loading Widgets for Ipython Jupyter Notebook and Lab

Open source CSS Loading animations from [loading.io](https://loading.io/css/)

It uses `string.Template` for templates 
(https://docs.python.org/3.5/library/string.html)

It has 3 main parameters: `size`, `color`, and `background_color`. You can
add custom parameters in the subclass implementation.

It has three methods that can be overwritten by the subclasses in order to
implement custom css properties: `compute_size`, `compute_color` and
`compute_background_color`. This methods must return a `dict` holding the
'extra' parameters.

As an example, the `Ring` loading widget:

    class Ring(Loading):
        def __init__(self, border=None, **kwargs):
            css = """
            .lds-ring {
              display: inline-block;
              position: relative;
              width: ${width}px;
              height: ${height}px;
            }
            .lds-ring div {
              box-sizing: border-box;
              display: block;
              position: absolute;
              width: ${inner_width}px;
              height: ${inner_height}px;
              margin: ${margin}px;
              border: $border solid ${color};
              border-radius: 50%;
              animation: lds-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
              border-color: ${color} transparent transparent transparent;
              background-color: ${background_color};
            }
            .lds-ring div:nth-child(1) {
              animation-delay: -0.45s;
            }
            .lds-ring div:nth-child(2) {
              animation-delay: -0.3s;
            }
            .lds-ring div:nth-child(3) {
              animation-delay: -0.15s;
            }
            @keyframes lds-ring {
              0% {
                transform: rotate(0deg);
              }
              100% {
                transform: rotate(360deg);
              }
            }
            """
            html = """
            <div class="lds-ring">
              <div></div>
              <div></div>
              <div></div>
              <div></div>
            </div>
            """
            self.border = border
            super(Ring, self).__init__(css=css, html=html, **kwargs)
    
        def compute_size(self, size):
    
            width = size
            height = size
            inner_width = int(size*0.8)
            inner_height = int(size*0.8)
            border = self.border if self.border else int(size*0.1)
            margin = border
            extra = dict(inner_width=inner_width, inner_height=inner_height,
                         margin=margin, border=border, width=width, height=height)
            return extra

