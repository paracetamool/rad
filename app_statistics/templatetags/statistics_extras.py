from django import template
from user_agents import parse

register = template.Library()


@register.filter(name="getBrowserName")
def getBrowserName(value):
    return str(parse(value).browser.family)


@register.filter(name="getBrowserVersion")
def getBrowserVersion(value):
    return str(parse(value).browser.version_string)


@register.filter(name="getOsName")
def getOsName(value):
    return str(parse(value).os.family)


@register.filter(name="getOsVersion")
def getOsVersion(value):
    return str(parse(value).os.version_string)


@register.filter(name="getDeviceName")
def getDeviceName(value):
    return str(parse(value).device.family)


@register.filter(name="getDocName")
def getDocName(value):
    return value.split('/')[-1]
