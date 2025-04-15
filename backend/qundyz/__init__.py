try:
    from .settings.development import *
except ImportError:
    from .settings.production import *