try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *
try:
    import Products.CMFCore.permissions as CMFCorePermissions
except ImportError:
    from Products.CMFCore import CMFCorePermissions
from AccessControl import ClassSecurityInfo
from Products.PloneHelpCenter.config import *
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_hasattr, base_hasattr
from AccessControl import getSecurityManager
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from zope.interface import implements
from Products.PloneHelpCenter.interfaces import IHelpCenterFolder

# Compare section brains by title
def _sectionCmp(a, b):
    # depends on cmp(True, False) == 1
    ash = getattr(a, 'getStartHere', False)
    bsh = getattr(b, 'getStartHere', False)
    if ash == bsh:
        return cmp(a.Title.lower(), b.Title.lower())
    elif ash:
        return -1
    else:
        return 1


class PHCFolder(BrowserDefaultMixin):
    """A simple mixin for folderish archetype"""

    implements(IHelpCenterFolder)
    __implements__ = BrowserDefaultMixin.__implements__

    _at_rename_after_creation = True

    # empty right slot by default
    _properties = OrderedBaseFolder._properties +  (
        {'id'    : 'right_slots',
         'type'  : 'lines',
         'mode'  : 'rw',
         'label' : 'Right slots'
         },
         )

    security = ClassSecurityInfo()

    security.declareProtected(CMFCorePermissions.View, 'getAudiencesVocab')
    def getAudiencesVocab(self):
        """Get sections vocabulary."""
        if not safe_hasattr(self.aq_parent, 'getAudiencesVocab'):
            return []
        return self.aq_parent.getAudiencesVocab()


    security.declareProtected(CMFCorePermissions.View, 'getVersionsVocab')
    def getVersionsVocab(self):
        """Get version vocabulary."""
        if not safe_hasattr(self.aq_parent, 'getVersionsVocab'):
            return []
        return self.aq_parent.getVersionsVocab()
            

    security.declareProtected(CMFCorePermissions.View, 'getSectionsVocab')
    def getSectionsVocab(self):
        """Get sections vocabulary"""
        
        localSections = self.sectionsVocab
        if len(localSections):
            return localSections
        elif base_hasattr(self.aq_parent, 'getSectionsVocab'):
            return self.aq_parent.sectionsVocab
        else:
            return ()
