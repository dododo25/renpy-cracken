# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This file contains code for initializing and managing the display
# window.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

import renpy.display

class IgnoreEvent(Exception):
    """
    Exception that is raised when we want to ignore an event, but
    also don't want to return anything.
    """

    pass

class EndInteraction(Exception):
    """
    Exception that can be raised (for example, during the render method of
    a displayable) to end the current interaction immediately.
    """

    def __init__(self, value):
        self.value = value

class absolute(float):
    """
    This represents an absolute float coordinate.
    """
    __slots__ = [ ]

class DisplayableArguments(renpy.object.Object):
    """
    Represents a set of arguments that can be passed to a duplicated
    displayable.
    """

    # The name of the displayable without any arguments.
    name = ()

    # Arguments supplied.
    args = ()

    # The style prefix in play. This is used by DynamicImage to figure
    # out the prefix list to apply.
    prefix = None

    # True if lint is in use.
    lint = False

class Displayable(renpy.object.Object):
    """
    The base class for every object in Ren'Py that can be
    displayed to the screen.

    Drawables will be serialized to a savegame file. Therefore, they
    shouldn't store non-serializable things (like pygame surfaces) in
    their fields.
    """

    # Some invariants about method call order:
    #
    # per_interact is called before render.
    # render is called before event.
    #
    # get_placement can be called at any time, so can't
    # assume anything.

    # If True this displayable can accept focus.
    # If False, it can't, but it keeps its place in the focus order.
    # If None, it does not have a place in the focus order.
    focusable = None

    # This is the focus named assigned by the focus code.
    full_focus_name = None

    # A role ('selected_' or '' that prefixes the style).
    role = ''

    # The event we'll pass on to our parent transform.
    transform_event = None

    # Can we change our look in response to transform_events?
    transform_event_responder = False

    # The main displayable, if this displayable is the root of a composite
    # displayable. (This is used by SL to figure out where to add children
    # to.) If None, it is itself.
    _main = None

    # A list of the children that make up this composite displayable.
    _composite_parts = [ ]

    # The location the displayable was created at, if known.
    _location = None

    # Does this displayable use the scope?
    _uses_scope = False

    # Arguments supplied to this displayable.
    _args = DisplayableArguments()

    # Set to true of the displayable is duplicatable (has a non-trivial
    # duplicate method), or one of its children is.
    _duplicatable = False

    # Does this displayable require clipping?
    _clipping = False

    # Does this displayable have a tooltip?
    _tooltip = None

    def __init__(self, focus=None, default=False, style='default', _args=None, tooltip=None, default_focus=False, **properties):
        global default_style

        if (style == "default") and (not properties):
            self.style = default_style
        else:
            self.style = renpy.style.Style(style, properties) # @UndefinedVariable

        self.focus_name = focus
        self.default = default or default_focus
        self._tooltip = tooltip

        if _args is not None:
            self._args = _args

class SceneListEntry(renpy.object.Object):
    """
    Represents a scene list entry. Since this was replacing a tuple,
    it should be treated as immutable after its initial creation.
    """

    def __init__(self, tag, zorder, show_time, animation_time, displayable, name):
        self.tag = tag
        self.zorder = zorder
        self.show_time = show_time
        self.animation_time = animation_time
        self.displayable = displayable
        self.name = name

class SceneLists(renpy.object.Object):
    """
    This stores the current scene lists that are being used to display
    things to the user.
    """

    __version__ = 7

    def __init__(self, oldsl, shown):
        super(SceneLists, self).__init__()

        # Has a window been shown as part of these scene lists?
        self.shown_window = False

        # A map from layer name -> list(SceneListEntry)
        self.layers = { }

        # A map from layer name -> tag -> at_list associated with that tag.
        self.at_list = { }

        # A map from layer to (start time, at_list), where the at list has
        # been applied to the layer as a whole.
        self.layer_at_list = { }

        # The camera list, which is similar to the layer at list but is not
        # cleared during the scene statement.
        self.camera_list = { }

        # The current shown images,
        self.shown = shown

        # A list of (layer, tag) pairs that are considered to be
        # transient.
        self.additional_transient = [ ]

        # Either None, or a DragGroup that's used as the default for
        # drags with names.
        self.drag_group = None

        # A map from a layer to the transform that applies to that
        # layer.
        self.layer_transform = { }

        # Same thing, but for the camera transform.
        self.camera_transform = { }

        if oldsl:
            for i in renpy.config.layers + renpy.config.top_layers:
                try:
                    self.layers[i] = oldsl.layers[i][:]
                except KeyError:
                    self.layers[i] = [ ]

                if i in oldsl.at_list:
                    self.at_list[i] = oldsl.at_list[i].copy()
                    self.layer_at_list[i] = oldsl.layer_at_list[i]
                    self.camera_list[i] = oldsl.camera_list[i]
                else:
                    self.at_list[i] = { }
                    self.layer_at_list[i] = (None, [ ])
                    self.camera_list[i] = (None, [ ])

            for i in renpy.config.overlay_layers:
                self.clear(i)

            self.replace_transient(prefix=None)

            self.focused = None

            self.drag_group = oldsl.drag_group

            self.layer_transform.update(oldsl.layer_transform)
            self.camera_transform.update(oldsl.camera_transform)
        else:
            for i in renpy.config.layers + renpy.config.top_layers:
                self.layers[i] = [ ]
                self.at_list[i] = { }
                self.layer_at_list[i] = (None, [ ])
                self.camera_list[i] = (None, [ ])

            self.music = None
            self.focused = None

class MouseMove(object):
    """
    This contains information about the current mouse move.
    """

    def __init__(self, x, y, duration):
        self.start = get_time()

        if duration is not None:
            self.duration = duration
        else:
            self.duration = 0

        self.start_x, self.start_y = renpy.display.draw.get_mouse_pos()

        self.end_x = x
        self.end_y = y

class Renderer(object):
    """
    A Renderer (also known as a draw object) is responsible for drawing a
    tree of displayables to the window. It also provides other services that
    involved drawing and the SDL main window, as documented here.

    A Renderer is responsible for updating the renpy.game.preferences.fullscreen
    and renpy.game.preferences.physical_size preferences, when these are
    changed from outside the game.

    A renderer has an info dict, that contains the keys from pygame_sdl2.display.Info(),
    and then:
    - "renderer", the name of the Renderer.
    - "resizable", true if the window can be resized.
    - "additive", true if additive blendering is supported.
    - "models", true if model-based rendering is being used.
    """

class Interface(object):
    """
    This represents the user interface that interacts with the user.
    It manages the Display objects that display things to the user, and
    also handles accepting and responding to user input.

    @ivar display: The display that we used to display the screen.

    @ivar profile_time: The time of the last profiling.

    @ivar screenshot: A screenshot, or None if no screenshot has been
    taken.

    @ivar old_scene: The last thing that was displayed to the screen.

    @ivar transition: A map from layer name to the transition that will
    be applied the next time interact restarts.

    @ivar transition_time: A map from layer name to the time the transition
    involving that layer started.

    @ivar transition_from: A map from layer name to the scene that we're
    transitioning from on that layer.

    @ivar suppress_transition: If True, then the next transition will not
    happen.

    @ivar force_redraw: If True, a redraw is forced.

    @ivar restart_interaction: If True, the current interaction will
    be restarted.

    @ivar pushed_event: If not None, an event that was pushed back
    onto the stack.

    @ivar mouse: The name of the mouse cursor to use during the current
    interaction.

    @ivar ticks: The number of 20hz ticks.

    @ivar frame_time: The time at which we began drawing this frame.

    @ivar interact_time: The time of the start of the first frame of the current interact_core.

    @ivar time_event: A singleton ignored event.

    @ivar event_time: The time of the current event.

    @ivar timeout_time: The time at which the timeout will occur.
    """

    def __init__(self):
        # PNG data and the surface for the current file screenshot.
        self.screenshot = None
        self.screenshot_surface = None

        self.old_scene = { }
        self.transition = { }
        self.ongoing_transition = { }
        self.transition_time = { }
        self.transition_from = { }
        self.suppress_transition = False
        self.quick_quit = False
        self.force_redraw = False
        self.restart_interaction = False
        self.pushed_event = None
        self.ticks = 0
        self.mouse = 'default'
        self.timeout_time = None
        self.last_event = None
        self.current_context = None
        self.roll_forward = None

        # Are we in fullscreen mode?
        self.fullscreen = False

        # Things to be preloaded.
        self.preloads = [ ]

        # The time at which this object was initialized.
        self.init_time = get_time()

        # The time at which this draw occurs.
        self.frame_time = 0

        # The time when this interaction occured.
        self.interact_time = None

        # The time we last tried to quit.
        self.quit_time = 0

        # Are we currently processing the quit event?
        self.in_quit_event = False

        self.time_event = pygame.event.Event(TIMEEVENT, { "modal" : False })
        self.redraw_event = pygame.event.Event(REDRAW)

        # Are we focused?
        self.mouse_focused = True
        self.keyboard_focused = True

        # Properties for each layer.
        self.layer_properties = { }

        # Have we shown the window this interaction?
        self.shown_window = False

        # Should we ignore the rest of the current touch? Used to ignore the
        # rest of a mousepress after a longpress occurs.
        self.ignore_touch = False

        # Should we clear the screenshot at the start of the next interaction?
        self.clear_screenshot = False

        for layer in renpy.config.layers + renpy.config.top_layers:
            if layer in renpy.config.layer_clipping:
                x, y, w, h = renpy.config.layer_clipping[layer]
                self.layer_properties[layer] = dict(
                    xpos=x,
                    xanchor=0,
                    ypos=y,
                    yanchor=0,
                    xmaximum=w,
                    ymaximum=h,
                    xminimum=w,
                    yminimum=h,
                    clipping=True,
                    )

            else:
                self.layer_properties[layer] = dict()

        # A stack giving the values of self.transition and self.transition_time
        # for contexts outside the current one. This is used to restore those
        # in the case where nothing has changed in the new context.
        self.transition_info_stack = [ ]

        # The time when the event was dispatched.
        self.event_time = 0

        # The time we saw the last mouse event.
        self.mouse_event_time = None

        # Should we show the mouse?
        self.show_mouse = True

        # Should we reset the display?
        self.display_reset = False

        # Should we profile the next frame?
        self.profile_once = False

        # The thread that can do display operations.
        self.thread = threading.current_thread()

        # Init timing.
        init_time()
        self.mouse_event_time = get_time()

        # The current window caption.
        self.window_caption = None

        renpy.game.interface = self
        renpy.display.interface = self

        # Are we in safe mode, from holding down shift at start?
        self.safe_mode = False

        # Do we need a background screenshot?
        self.bgscreenshot_needed = False

        # Event used to signal background screenshot taken.
        self.bgscreenshot_event = threading.Event()

        # The background screenshot surface.
        self.bgscreenshot_surface = None

        # Mouse move. If not None, information about the current mouse
        # move.
        self.mouse_move = None

        # If in text editing mode, the current text editing event.
        self.text_editing = None

        # The text rectangle after the current draw.
        self.text_rect = None

        # The text rectangle after the previous draw.
        self.old_text_rect = None

        # Are we a touchscreen?
        self.touch = renpy.exports.variant("touch")

        # Should we use the touch keyboard?
        self.touch_keyboard = (self.touch and renpy.emscripten) or renpy.config.touch_keyboard

        # Should we restart the interaction?
        self.restart_interaction = True

        # For compatibility with older code.
        if renpy.config.periodic_callback:
            renpy.config.periodic_callbacks.append(renpy.config.periodic_callback)

        # Has start been called?
        self.started = False

        # Are we in fullscreen video mode?
        self.fullscreen_video = False

        self.safe_mode = get_safe_mode()
        renpy.safe_mode_checked = True

        # A scale factor used to compensate for the system DPI.
        self.dpi_scale = self.setup_dpi_scaling()

        renpy.display.log.write("DPI scale factor: %f", self.dpi_scale)

        # A time until which we should draw at maximum framerate.
        self.maximum_framerate_time = 0.0
        self.maximum_framerate(initial_maximum_framerate)

        # True if this is the first interact.
        self.start_interact = True

        # The time of each frame.
        self.frame_times = [ ]

        # The duration of each frame, in seconds.
        self.frame_duration = 1.0 / 60.0

        # The cursor cache.
        self.cursor_cache = None

        # The old mouse.
        self.old_mouse = None

        # A map from a layer to the duration of the current transition on that
        # layer.
        self.transition_delay = { }

        # Is this the first frame?
        self.first_frame = True

        try:
            self.setup_nvdrs()
        except:
            pass
