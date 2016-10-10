# -*- coding: utf-8 -*-
# (c) 2013,2014 Andreas Motl, Elmyra UG
import logging
from pyramid.threadlocal import get_current_request
from pyramid.url import route_url
from akhet.urlgenerator import URLGenerator as ApplicationURLGenerator

from . import helpers

site_version = '0.0.0'

log = logging.getLogger(__name__)


def includeme(config):
    """Configure all application-specific subscribers."""
    config.add_subscriber(create_url_generators, "pyramid.events.ContextFound")
    config.add_subscriber(create_tools, "pyramid.events.ContextFound")
    config.add_subscriber(add_renderer_globals, "pyramid.events.BeforeRender")
    config.add_subscriber(add_html_foundation, "pyramid.events.BeforeRender")


def create_url_generators(event):
    """A subscriber for ``pyramid.events.ContextFound`` events. I create various
    URL generators and attach them to the request.
    Templates and views can then use them to generate application URLs.

    - ``request.url_generator``: Generates URLs to application routes
    - ``request.blob_url_generator``: Generates URLs to the ``BlobStore`
    """

    request = event.request
    context = request.context

    app_url_generator = ApplicationURLGenerator(context, request, qualified=False)
    request.url_generator = app_url_generator

    #blob_url_generator = BlobURLGenerator(context, request, qualified=False)
    #request.blob_url_generator = blob_url_generator


def create_tools(event):
    """A subscriber for ``pyramid.events.ContextFound`` events. I create various
    tools and attach them to the request.

    - ``request.geolocator``: Queries geolocation service for geographic position
    """
    request = event.request
    #request.geolocator = GeoLocator(request)


def add_renderer_globals(event):
    """A subscriber for ``pyramid.events.BeforeRender`` events.  I add
    some :term:`renderer globals` with values that are familiar to Pylons
    users.
    """

    # use event as renderer globals
    renderer_globals = event

    # initialize fanstatic
    #needed = fanstatic.init_needed(base_url='http://localhost:6543')
    #renderer_globals["needed"] = needed

    renderer_globals["h"] = helpers
    request = event.get("request") or get_current_request()
    if not request:     # pragma: no cover
        return
    renderer_globals["r"] = request
    renderer_globals["url"] = request.url_generator
    #renderer_globals["bloburl"] = request.blob_url_generator

    # Optional additions:
    #renderer_globals["settings"] = request.registry.settings
    #try:
    #    renderer_globals["session"] = request.session
    #except ConfigurationError:
    #    pass
    #renderer_globals["c"] = request.tmpl_context

    # Page title
    renderer_globals['theme'] = helpers.Bootstrapper().theme_parameters()
    renderer_globals['page_title'] = None


def add_html_foundation(event):

    # setup javascript foundation

    # underscore.string
    from js.underscore_string import underscore_string
    underscore_string.need()

    # backbone.marionette
    from js.marionette import marionette
    marionette.need()

    # jquery
    #from js.jquery import jquery
    #jquery.need()
    from js.jquery_shorten import jquery_shorten
    jquery_shorten.need()
    from js.purl import purl
    purl.need()

    from js.select2 import select2
    select2.need()

    # jqueryui
    #from js.jqueryui import jqueryui, base as jqueryui_base, smoothness as jqueryui_smoothness
    #from js.jqueryui_bootstrap import jqueryui_bootstrap
    #jqueryui.need()
    #jqueryui_base.need()
    #jqueryui_smoothness.need()
    #jqueryui_bootstrap.need()


    # setup css foundation

    # bootstrap
    from js.bootstrap import bootstrap, bootstrap_responsive_css
    #from js.bootstrap import bootstrap_theme
    bootstrap.need()
    #bootstrap_theme.need()
    bootstrap_responsive_css.need()

    # fontawesome
    from css.fontawesome import fontawesome
    fontawesome.need()
