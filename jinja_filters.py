from jinja2.utils import Markup

def authors(value):

  if len(value) > 2:
    authors = '%s, %s' % (value[0], value[1])
    html = '<ul class="dropdown"><li>%s, et al.<ul>' % authors
    for i in range(len(value)-2):
      html += '<li>%s<li>' % value[i+2]
    html += '</ul></li></ul>'
  else:
    if len(value) == 2:
      authors = '%s, %s' % (value[0], value[1])
    elif len(value) == 1:
      authors = value[0]
    elif len(value) == 0:
      authors = 'Not Available'
    html = '<p>%s</p>' % authors
  return Markup(html)