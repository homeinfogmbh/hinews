# ./dom.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:054fee2b439c162e79f325c94546464bb0a4905e
# Generated 2018-02-05 11:16:20.777585 by PyXB version 1.2.6-DEV using Python 3.6.4.final.0
# Namespace http://xml.homeinfo.de/schema/hinews

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:9c6cb766-0a5d-11e8-9a16-7427eaa9df7d')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6-DEV'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://xml.homeinfo.de/schema/hinews', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Complex type {http://xml.homeinfo.de/schema/hinews}News with content type ELEMENT_ONLY
class News (pyxb.binding.basis.complexTypeDefinition):
    """
                A list of articles.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'News')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 9, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element article uses Python identifier article
    __article = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'article'), 'article', '__httpxml_homeinfo_deschemahinews_News_article', True, pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 16, 12), )

    
    article = property(__article.value, __article.set, None, None)

    _ElementMap.update({
        __article.name() : __article
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.News = News
Namespace.addCategoryObject('typeBinding', 'News', News)


# Complex type {http://xml.homeinfo.de/schema/hinews}Article with content type ELEMENT_ONLY
class Article (pyxb.binding.basis.complexTypeDefinition):
    """
                A news article.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Article')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 21, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element text uses Python identifier text
    __text = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'text'), 'text', '__httpxml_homeinfo_deschemahinews_Article_text', False, pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 28, 12), )

    
    text = property(__text.value, __text.set, None, '\n                        The article text.\n                    ')

    
    # Element source uses Python identifier source
    __source = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'source'), 'source', '__httpxml_homeinfo_deschemahinews_Article_source', False, pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 35, 12), )

    
    source = property(__source.value, __source.set, None, "\n                        The article's source.\n                    ")

    
    # Element tags uses Python identifier tags
    __tags = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'tags'), 'tags', '__httpxml_homeinfo_deschemahinews_Article_tags', True, pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 42, 12), )

    
    tags = property(__tags.value, __tags.set, None, "\n                        The article's tags.\n                    ")

    
    # Element images uses Python identifier images
    __images = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'images'), 'images', '__httpxml_homeinfo_deschemahinews_Article_images', True, pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 49, 12), )

    
    images = property(__images.value, __images.set, None, "\n                        The article's images.\n                    ")

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpxml_homeinfo_deschemahinews_Article_id', pyxb.binding.datatypes.integer, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 57, 8)
    __id._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 57, 8)
    
    id = property(__id.value, __id.set, None, "\n                    The article's ID.\n                ")

    
    # Attribute title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'title'), 'title', '__httpxml_homeinfo_deschemahinews_Article_title', pyxb.binding.datatypes.string, required=True)
    __title._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 64, 8)
    __title._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 64, 8)
    
    title = property(__title.value, __title.set, None, "\n                    The article's title.\n                ")

    
    # Attribute subtitle uses Python identifier subtitle
    __subtitle = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'subtitle'), 'subtitle', '__httpxml_homeinfo_deschemahinews_Article_subtitle', pyxb.binding.datatypes.string)
    __subtitle._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 71, 8)
    __subtitle._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 71, 8)
    
    subtitle = property(__subtitle.value, __subtitle.set, None, "\n                    The article's subtitle.\n                ")

    
    # Attribute created uses Python identifier created
    __created = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'created'), 'created', '__httpxml_homeinfo_deschemahinews_Article_created', pyxb.binding.datatypes.dateTime, required=True)
    __created._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 78, 8)
    __created._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 78, 8)
    
    created = property(__created.value, __created.set, None, "\n                    The article's creation time.\n                ")

    
    # Attribute active_from uses Python identifier active_from
    __active_from = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'active_from'), 'active_from', '__httpxml_homeinfo_deschemahinews_Article_active_from', pyxb.binding.datatypes.date)
    __active_from._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 85, 8)
    __active_from._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 85, 8)
    
    active_from = property(__active_from.value, __active_from.set, None, '\n                    Date from which on the article is active.\n                ')

    
    # Attribute active_until uses Python identifier active_until
    __active_until = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'active_until'), 'active_until', '__httpxml_homeinfo_deschemahinews_Article_active_until', pyxb.binding.datatypes.date)
    __active_until._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 92, 8)
    __active_until._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 92, 8)
    
    active_until = property(__active_until.value, __active_until.set, None, '\n                    Date from which on the article is no longer active.\n                ')

    _ElementMap.update({
        __text.name() : __text,
        __source.name() : __source,
        __tags.name() : __tags,
        __images.name() : __images
    })
    _AttributeMap.update({
        __id.name() : __id,
        __title.name() : __title,
        __subtitle.name() : __subtitle,
        __created.name() : __created,
        __active_from.name() : __active_from,
        __active_until.name() : __active_until
    })
_module_typeBindings.Article = Article
Namespace.addCategoryObject('typeBinding', 'Article', Article)


# Complex type {http://xml.homeinfo.de/schema/hinews}Image with content type ELEMENT_ONLY
class Image (pyxb.binding.basis.complexTypeDefinition):
    """
                An article's image.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Image')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 102, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element source uses Python identifier source
    __source = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'source'), 'source', '__httpxml_homeinfo_deschemahinews_Image_source', False, pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 109, 12), )

    
    source = property(__source.value, __source.set, None, "\n                        The image's source.\n                    ")

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpxml_homeinfo_deschemahinews_Image_id', pyxb.binding.datatypes.integer, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 117, 8)
    __id._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 117, 8)
    
    id = property(__id.value, __id.set, None, "\n                    The image's ID.\n                ")

    
    # Attribute uploaded uses Python identifier uploaded
    __uploaded = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'uploaded'), 'uploaded', '__httpxml_homeinfo_deschemahinews_Image_uploaded', pyxb.binding.datatypes.dateTime, required=True)
    __uploaded._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 124, 8)
    __uploaded._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 124, 8)
    
    uploaded = property(__uploaded.value, __uploaded.set, None, "\n                    The image's upload date and time.\n                ")

    _ElementMap.update({
        __source.name() : __source
    })
    _AttributeMap.update({
        __id.name() : __id,
        __uploaded.name() : __uploaded
    })
_module_typeBindings.Image = Image
Namespace.addCategoryObject('typeBinding', 'Image', Image)


news = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'news'), News, location=pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 6, 4))
Namespace.addCategoryObject('elementBinding', news.name().localName(), news)



News._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'article'), Article, scope=News, location=pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 16, 12)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 16, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(News._UseForTag(pyxb.namespace.ExpandedName(None, 'article')), pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 16, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
News._Automaton = _BuildAutomaton()




Article._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'text'), pyxb.binding.datatypes.string, scope=Article, documentation='\n                        The article text.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 28, 12)))

Article._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'source'), pyxb.binding.datatypes.string, scope=Article, documentation="\n                        The article's source.\n                    ", location=pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 35, 12)))

Article._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'tags'), pyxb.binding.datatypes.string, scope=Article, documentation="\n                        The article's tags.\n                    ", location=pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 42, 12)))

Article._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'images'), Image, scope=Article, documentation="\n                        The article's images.\n                    ", location=pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 49, 12)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 42, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 49, 12))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Article._UseForTag(pyxb.namespace.ExpandedName(None, 'text')), pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 28, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Article._UseForTag(pyxb.namespace.ExpandedName(None, 'source')), pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 35, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Article._UseForTag(pyxb.namespace.ExpandedName(None, 'tags')), pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 42, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Article._UseForTag(pyxb.namespace.ExpandedName(None, 'images')), pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 49, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Article._Automaton = _BuildAutomaton_()




Image._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'source'), pyxb.binding.datatypes.string, scope=Image, documentation="\n                        The image's source.\n                    ", location=pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 109, 12)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Image._UseForTag(pyxb.namespace.ExpandedName(None, 'source')), pyxb.utils.utility.Location('/home/neumann/Projects/hinews/doc/news.xsd', 109, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Image._Automaton = _BuildAutomaton_2()

