def render_header(http_request, admin=False):
    # only while rendering isn't a thing
    if not admin:
        return '<html lang="en-US"><head><link rel="stylesheet" href="/staticfiles/frontpage/style.css"></head>' \
               '<body><header class="header">C3FOC site</header>'
    else:
        # return the same for now
        return '<html lang="en-US"><head><link rel="stylesheet" href="/staticfiles/frontpage/style.css"></head>' \
               '<body><header class="header">C3FOC site</header>'
