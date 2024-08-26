from fasthtml.common import *

app, rt = fast_app()

@rt('/')
def index():
    return Div(H1('Welcome to STRATA-FIT'), P('This is the data validation app.'))

@rt('/validate')
def validate():
    return Form(
        Input(type='file', name='file'),
        Button('Upload', type='submit', hx_post='/validate', hx_target='#result'),
        Div(id='result')
    )

serve()
