from django import template

register = template.Library()

@register.simple_tag
def bootstrap_modal_show(domid):
    return """
    <button type="button" class="btn btn-default tool-button" aria-label="Left Align"
        data-toggle="modal" data-target="#%s">
      <span class="glyphicon glyphicon-question-sign" aria-hidden="true"></span>
    </button>""" % domid


@register.tag(name='bootstrap_modal')
def do_bootstrap_modal(parser, token):
    try:
        tag_name, title, domid = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires two arguments" % token.contents.split()[0]
    title = template.Variable(title)
    domid = template.Variable(domid)
    nodelist = parser.parse(("endbootstrap_modal",))
    parser.delete_first_token()
    return FormatBootstrapModal(title, domid, nodelist)

class FormatBootstrapModal(template.Node):
    html = """
    <div class="modal fade" id="%(domid)s" role="dialog">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-body">
                %(content)s
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
    """
    def __init__(self, title, domid, nodelist):
        self.title = title
        self.domid = domid
        self.nodelist = nodelist

    def render(self, context):
        content = self.nodelist.render(context)
        return FormatBootstrapModal.html % {'title': self.title, 'domid': self.domid, 'content': content}
