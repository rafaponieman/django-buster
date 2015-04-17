import json

from django import template
from .. import get_buster_json, get_buster_for_url

register = template.Library()


@register.tag
def buster(parser, token):
    nodelist = parser.parse(('endbuster',))
    parser.delete_first_token()
    return BusterNode(nodelist)


class BusterNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
        self.busters = get_buster_json()

    def render(self, context):
        url = self.nodelist.render(context)
        buster = get_buster_for_url(url, self.busters)
        if buster:
            return u'{0}?{1}'.format(url, buster)
        return url


@register.simple_tag
def busters_json():
    busters = get_buster_json()
    if busters:
        return json.dumps(busters)
    return 'null'
