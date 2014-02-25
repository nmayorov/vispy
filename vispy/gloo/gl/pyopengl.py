# -*- coding: utf-8 -*-
# Copyright (c) 2014, Vispy Development Team.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.

""" vispy.gloo.gl.desktop: namespace for OpenGL ES 2.0 API based on the
desktop OpenGL implementation.
"""

from . import _copy_gl_functions
from ._constants import *


## Compatibility


def glShaderSource_compat(handle, code):
    """ This version of glShaderSource applies small modifications
    to the given GLSL code in order to make it more compatible between
    desktop and ES2.0 implementations. Specifically:
      * It sets the #version pragma (if none is given already)
      * It returns a (possibly empty) set of enums that should be enabled
        (for automatically enabling point sprites)
    """

    # Make a string
    if isinstance(code, (list, tuple)):
        code = '\n'.join(code)

    # Determine whether this is a vertex or fragment shader
    code_ = '\n' + code
    is_vertex = '\nattribute' in code_
    is_fragment = not is_vertex

    # Determine whether to write the #version pragma
    write_version = True
    for line in code.splitlines():
        if line.startswith('#version'):
            write_version = False
            logger.warn('For compatibility accross different GL backends, ' +
                        'avoid using the #version pragma.')
    if write_version:
        code = '#version 120\n#line 0\n' + code

    # Do the call
    glShaderSource(handle, [code])

    # Determine whether to activate point sprites
    enums = set()
    if is_fragment and 'gl_PointCoord' in code:
        enums.add(Enum('GL_VERTEX_PROGRAM_POINT_SIZE', 34370))
        enums.add(Enum('GL_POINT_SPRITE', 34913))
    return enums
    return []


def _patch():
    """ Monkey-patch pyopengl to fix a bug in glBufferSubData. """
    import sys
    from OpenGL import GL
    if sys.version_info > (3,):
        buffersubdatafunc = GL.glBufferSubData
        if hasattr(buffersubdatafunc, 'wrapperFunction'):
            buffersubdatafunc = buffersubdatafunc.wrapperFunction
        _m = sys.modules[buffersubdatafunc.__module__]
        _m.long = int


## Inject


from . import _pyopengl
_copy_gl_functions(_pyopengl, globals())

_patch()
