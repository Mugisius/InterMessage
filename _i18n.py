import gettext
import os

translation = gettext.translation("IM", os.path.abspath('./po'), fallback=True)
_ = translation.gettext
