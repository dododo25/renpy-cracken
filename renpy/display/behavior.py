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

# This contains various Displayables that handle events.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

import renpy.text.text
import renpy.display.core
import renpy.display.layout
import renpy.python
import renpy.ui

##############################################################################
# Special-Purpose Displayables

class Keymap(renpy.display.layout.Null):
    """
    This is a behavior that maps keys to actions that are called when
    the key is pressed. The keys are specified by giving the appropriate
    k_constant from pygame.constants, or the unicode for the key.
    """

    def __init__(self, replaces=None, activate_sound=None, **keymap):
        if activate_sound is not None:
            super(Keymap, self).__init__(style='default', activate_sound=activate_sound)
        else:
            super(Keymap, self).__init__(style='default')

        self.keymap = keymap

class RollForward(renpy.display.layout.Null):
    """
    This behavior implements rollforward.
    """

    def __init__(self, value, **properties):
        super(RollForward, self).__init__(**properties)
        self.value = value

class PauseBehavior(renpy.display.layout.Null):
    """
    This is a class implementing the Pause behavior, which is to
    return a value after a certain amount of time has elapsed.
    """

    voice = False

    def __init__(self, delay, result=False, voice=False, **properties):
        super(PauseBehavior, self).__init__(**properties)

        self.delay = delay
        self.result = result
        self.voice = voice

class SoundStopBehavior(renpy.display.layout.Null):
    """
    This is a class implementing the sound stop behavior,
    which is to return False when a sound is no longer playing
    on the named channel.
    """

    def __init__(self, channel, result=False, **properties):
        super(SoundStopBehavior, self).__init__(**properties)

        self.channel = channel
        self.result = result

class SayBehavior(renpy.display.layout.Null):
    """
    This is a class that implements the say behavior,
    which is to return True (ending the interaction) if
    the user presses space or enter, or clicks the left
    mouse button.
    """

    focusable = True
    text = None

    dismiss_unfocused = [ 'dismiss_unfocused' ]

    def __init__(self, default=True, afm=None, dismiss=[ 'dismiss' ], allow_dismiss=None, dismiss_unfocused=[ 'dismiss_unfocused' ], **properties):
        super(SayBehavior, self).__init__(default=default, **properties)

        if not isinstance(dismiss, (list, tuple)):
            dismiss = [ dismiss ]

        if not isinstance(dismiss_unfocused, (list, tuple)):
            dismiss_unfocused = [ dismiss_unfocused ]

        if afm is not None:
            self.afm_length = len(afm)
        else:
            self.afm_length = None

        # What keybindings lead to dismissal?
        self.dismiss = dismiss
        self.dismiss_unfocused = dismiss_unfocused

        self.allow_dismiss = allow_dismiss

##############################################################################
# Button

class Button(renpy.display.layout.Window):

    keymap = { }
    action = None
    alternate = None

    longpress_start = None
    longpress_x = None
    longpress_y = None

    role_parameter = None

    keysym = None
    alternate_keysym = None

    # This locks the displayable against further change.
    locked = False

    def __init__(self, 
                 child=None, 
                 style='button', 
                 clicked=None, 
                 hovered=None, 
                 unhovered=None, 
                 action=None, 
                 role=None,
                 time_policy=None, 
                 keymap={}, 
                 alternate=None,
                 selected=None, 
                 sensitive=None, 
                 keysym=None, 
                 alternate_keysym=None,
                 **properties):
        if isinstance(clicked, renpy.ui.Action):
            action = clicked

        super(Button, self).__init__(child, style=style, **properties)

        self.action = action
        self.selected = selected
        self.sensitive = sensitive
        self.clicked = clicked
        self.hovered = hovered
        self.unhovered = unhovered
        self.alternate = alternate

        self.focusable = True # (clicked is not None) or (action is not None)
        self.role_parameter = role

        self.keymap = keymap

        self.keysym = keysym
        self.alternate_keysym = alternate_keysym

        self.time_policy_data = None

        self._duplicatable = False

# Reimplementation of the TextButton widget as a Button and a Text
# widget.

class ImageButton(Button):
    """
    Used to implement the guts of an image button.
    """

    def __init__(self,
                 idle_image,
                 hover_image=None,
                 insensitive_image=None,
                 activate_image=None,
                 selected_idle_image=None,
                 selected_hover_image=None,
                 selected_insensitive_image=None,
                 selected_activate_image=None,
                 style='image_button',
                 clicked=None,
                 hovered=None,
                 **properties):

        hover_image = hover_image or idle_image
        insensitive_image = insensitive_image or idle_image
        activate_image = activate_image or hover_image

        selected_idle_image = selected_idle_image or idle_image
        selected_hover_image = selected_hover_image or hover_image
        selected_insensitive_image = selected_insensitive_image or insensitive_image
        selected_activate_image = selected_activate_image or activate_image

        self.state_children = dict(
            idle_=renpy.easy.displayable(idle_image),
            hover_=renpy.easy.displayable(hover_image),
            insensitive_=renpy.easy.displayable(insensitive_image),
            activate_=renpy.easy.displayable(activate_image),

            selected_idle_=renpy.easy.displayable(selected_idle_image),
            selected_hover_=renpy.easy.displayable(selected_hover_image),
            selected_insensitive_=renpy.easy.displayable(selected_insensitive_image),
            selected_activate_=renpy.easy.displayable(selected_activate_image),
            )

        super(ImageButton, self).__init__(None,
                                          style=style,
                                          clicked=clicked,
                                          hovered=hovered,
                                          **properties)

# This is used for an input that takes its focus from a button.
class HoveredProxy(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

class CaretBlink(renpy.display.core.Displayable):
    """
    A displayable that renders the caret.
    """

    def __init__(self, caret, caret_blink, **properties):
        properties.setdefault("yalign", 0.0)

        super(CaretBlink, self).__init__(**properties)
        caret = renpy.easy.displayable(caret)

        if caret._duplicatable:
            caret = caret._duplicate()
            caret._unique()

        self.caret = caret
        self.caret_blink = caret_blink

        self.st_base = 0

class Input(renpy.text.text.Text): # @UndefinedVariable
    """
    This is a Displayable that takes text as input.
    """

    changed = None
    prefix = ""
    suffix = ""
    caret_pos = 0
    old_caret_pos = 0
    pixel_width = None
    default = u""
    edit_text = u""
    value = None
    shown = False

    st = 0

    def __init__(self,
                 default="",
                 length=None,
                 style='input',
                 allow=None,
                 exclude=None,
                 prefix="",
                 suffix="",
                 changed=None,
                 button=None,
                 replaces=None,
                 editable=True,
                 pixel_width=None,
                 value=None,
                 copypaste=False,
                 caret_blink=None,
                 **properties):

        super(Input, self).__init__("", style=style, replaces=replaces, substitute=False, **properties)

        if caret_blink is None:
            caret_blink = renpy.config.input_caret_blink

        if value:
            self.value = value
            changed = value.set_text
            default = value.get_text()

        self.default = str(default)
        self.content = self.default

        self.length = length

        self.allow = allow
        self.exclude = exclude
        self.prefix = prefix
        self.suffix = suffix
        self.copypaste = copypaste

        self.changed = changed

        self.editable = editable
        self.pixel_width = pixel_width

        caretprops = { 'color' : None }

        for i in properties:
            if i.endswith("color"):
                caretprops[i] = properties[i]

        caret = renpy.display.image.Solid(xsize=1, style=style, **caretprops)

        if caret_blink:
            caret = CaretBlink(caret, caret_blink)

        self.caret = caret
        self.caret_pos = len(self.content)
        self.old_caret_pos = self.caret_pos

        if button:
            self.editable = False
            button.hovered = HoveredProxy(self.enable, button.hovered)
            button.unhovered = HoveredProxy(self.disable, button.unhovered)

        if isinstance(replaces, Input):
            self.content = replaces.content
            self.editable = replaces.editable
            self.caret_pos = replaces.caret_pos
            self.shown = replaces.shown

        self.update_text(self.content, self.editable)

# This class contains information about an adjustment that can change the
# position of content.

class Adjustment(renpy.object.Object):
    """
    :doc: ui
    :name: ui.adjustment class

    Adjustment objects represent a value that can be adjusted by a bar
    or viewport. They contain information about the value, the range
    of the value, and how to adjust the value in small steps and large
    pages.


    """

    force_step = False

    def __init__(self, range=1, value=0, step=None, page=None, changed=None, adjustable=None, ranged=None, force_step=False): # @ReservedAssignment
        """
        The following parameters correspond to fields or properties on
        the adjustment object:

        `range`
            The range of the adjustment, a number.

        `value`
            The value of the adjustment, a number.

        `step`
            The step size of the adjustment, a number. If None, then
            defaults to 1/10th of a page, if set. Otherwise, defaults
            to the 1/20th of the range.

            This is used when scrolling a viewport with the mouse wheel.

        `page`
            The page size of the adjustment. If None, this is set
            automatically by a viewport. If never set, defaults to 1/10th
            of the range.

            It's can be used when clicking on a scrollbar.

        The following parameters control the behavior of the adjustment.

        `adjustable`
            If True, this adjustment can be changed by a bar. If False,
            it can't.

            It defaults to being adjustable if a `changed` function
            is given or if the adjustment is associated with a viewport,
            and not adjustable otherwise.

        `changed`
            This function is called with the new value when the value of
            the adjustment changes.

        `ranged`
            This function is called with the adjustment object when
            the range of the adjustment is set by a viewport.

            This function may be called multiple times, as part of the layout
            process.

        `force_step`
            If True and this adjustment changes by dragging associated
            viewport or a bar, value will be changed only if the drag
            reached next step.
            If "release" and this adjustment changes by dragging associated
            viewport or a bar, after the release, value will be
            rounded to the nearest step.
            If False, this adjustment will changes by dragging, ignoring
            the step value.

        .. method:: change(value)

            Changes the value of the adjustment to `value`, updating
            any bars and viewports that use the adjustment.
         """
        super(Adjustment, self).__init__()

        if adjustable is None:
            if changed:
                adjustable = True

        self._range = range
        self._value = type(range)(value)
        self._page = page
        self._step = step
        self.changed = changed
        self.adjustable = adjustable
        self.ranged = ranged
        self.force_step = force_step

class Bar(renpy.display.core.Displayable):
    """
    Implements a bar that can display an integer value, and respond
    to clicks on that value.
    """

    __version__ = 2

    def __init__(self,
                 range=None, # @ReservedAssignment
                 value=None,
                 width=None,
                 height=None,
                 changed=None,
                 adjustment=None,
                 step=None,
                 page=None,
                 bar=None,
                 style=None,
                 vertical=False,
                 replaces=None,
                 hovered=None,
                 unhovered=None,
                 released=None,
                 **properties):
        self.value = None

        if adjustment is None:
            if isinstance(value, renpy.ui.BarValue):
                if isinstance(replaces, Bar):
                    value.replaces(replaces.value)

                self.value = value
                adjustment = value.get_adjustment()
                renpy.game.interface.timeout(0)

                tooltip = value.get_tooltip()
                if tooltip is not None:
                    properties.setdefault("tooltip", tooltip)
            else:
                adjustment = Adjustment(range, value, step=step, page=page, changed=changed)

        if style is None:
            if self.value is not None:
                if vertical:
                    style = self.value.get_style()[1]
                else:
                    style = self.value.get_style()[0]
            else:
                if vertical:
                    style = 'vbar'
                else:
                    style = 'bar'

        if width is not None:
            properties['xmaximum'] = width

        if height is not None:
            properties['ymaximum'] = height

        super(Bar, self).__init__(style=style, **properties)

        self.adjustment = adjustment
        self.focusable = True

        # These are set when we are first rendered.
        self.thumb_dim = 0
        self.height = 0
        self.width = 0
        self.hidden = False

        self.hovered = hovered
        self.unhovered = unhovered

        self.released = released

class Conditional(renpy.display.layout.Container):
    """
    This class renders its child if and only if the condition is
    true. Otherwise, it renders nothing. (Well, a Null).

    Warning: the condition MUST NOT update the game state in any
    way, as that would break rollback.
    """

    def __init__(self, condition, *args, **properties):
        super(Conditional, self).__init__(*args, **properties)

        self.condition = condition
        self.null = renpy.display.layout.Null()

        self.state = eval(self.condition, vars(renpy.store))

class TimerState(renpy.python.AlwaysRollback):
    """
    Stores the state of the timer, which may need to be rolled back.
    """

    started = False
    next_event = None

class Timer(renpy.display.layout.Null):

    __version__ = 1

    started = False

    def __init__(self, delay, action=None, repeat=False, args=(), kwargs={}, replaces=None, **properties):
        super(Timer, self).__init__(**properties)

        if delay <= 0:
            raise Exception("A timer's delay must be > 0.")

        # The delay.
        self.delay = delay

        # Should we repeat the event?
        self.repeat = repeat

        # The time the next event should occur.
        self.next_event = None

        # The function and its arguments.
        self.function = action
        self.args = args
        self.kwargs = kwargs

        # Did we start the timer?
        self.started = False

        if isinstance(replaces, Timer):
            self.state = replaces.state
        else:
            self.state = TimerState()

class MouseArea(renpy.display.core.Displayable):

    # The offset between st and at.
    at_st_offset = 0

    def __init__(self, hovered=None, unhovered=None, replaces=None, **properties):
        super(MouseArea, self).__init__(**properties)

        self.hovered = hovered
        self.unhovered = unhovered

        # Are we hovered right now?
        self.is_hovered = False

        if isinstance(replaces, MouseArea):
            self.is_hovered = replaces.is_hovered

        # Taken from the render.
        self.width = 0
        self.height = 0

class OnEvent(renpy.display.core.Displayable):
    """
    This is a displayable that runs an action in response to a transform
    event. It's used to implement the screen language on statement.
    """

    def __init__(self, event, action=[ ]):
        """
        `event`
            A string giving the event name.

        `action`
            An action or list of actions that are run when the event occurs.
        """
        super(OnEvent, self).__init__()

        self.event_name = event
        self.action = action
