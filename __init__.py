"""MetaHuman Facial Rig Transfer.

Standalone Blender extension that wraps a low-poly head cage onto an arbitrary
head mesh (ZWrap-style landmark + surface registration workflow), then
transfers the MetaHuman facial rig.

This file wires up the submodules.
"""

from . import props, prefs
from .core import render_state
from .ops import (op_load_cage, op_pairs, op_wrap, op_slide, op_live,
                  op_shading, op_skeleton, op_tune, op_mouth, op_morphs,
                  op_attach, op_weights, op_rig, op_merge, op_drivers, op_anim,
                  op_export, op_arkit, op_bake_drivers)
from .ui import overlay, panel, transition

# Order matters: props/prefs first so panels & ops can rely on them, and
# render_state before anything that stands down during a render.
_modules = (
    props,
    prefs,
    render_state,
    op_load_cage,
    op_pairs,
    op_wrap,
    op_slide,
    op_live,
    op_shading,
    op_skeleton,
    op_tune,
    op_mouth,
    op_morphs,
    op_attach,
    op_weights,
    op_rig,
    op_merge,
    op_drivers,
    op_anim,
    op_export,
    op_arkit,
    op_bake_drivers,
    transition,
    overlay,
    panel,
)


def register():
    for m in _modules:
        m.register()


def unregister():
    # One failing module must never protect the rest from unregistering -
    # a surviving depsgraph handler would keep driving rigs as a "ghost"
    # after the add-on is disabled or uninstalled.
    error = None
    for m in reversed(_modules):
        try:
            m.unregister()
        except Exception as exc:      # noqa: BLE001 - keep tearing down
            if error is None:
                error = exc
    if error is not None:
        raise error
