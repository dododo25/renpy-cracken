import loader
import os
import pickle

from renpy.ast import Init, Screen
from renpy.sl2.slast import SLDisplayable

def test_parse_sl_displayable_bar_statement():
    """
    screen test:
        bar left_bar "left.png" right_bar "right.png" <- this is our target block
    """
    expected = 'bar left_bar "left.png" right_bar "right.png"'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_displayable_as_bar.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen.nchildren[0]) == SLDisplayable
    assert expected == str(decompressed[0].block[0].screen.nchildren[0])

def test_parse_sl_displayable_vbar_statement():
    """
    screen test:
        vbar top_bar "top.png" bottom_bar "bottom.png" <- this is our target block
    """
    expected = 'vbar top_bar "top.png" bottom_bar "bottom.png"'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_displayable_as_vbar.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen.nchildren[0]) == SLDisplayable
    assert expected == str(decompressed[0].block[0].screen.nchildren[0])

def test_parse_sl_displayable_add_statement():
    """
    screen test:
        add "test.png" <- this is our target block
    """
    expected = 'add "test.png"'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_displayable_as_add.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen.nchildren[0]) == SLDisplayable
    assert expected == str(decompressed[0].block[0].screen.nchildren[0])

def test_parse_sl_displayable_null_statement():
    """
    screen test:
        null <- this is our target block
    """
    expected = 'null'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_displayable_as_null.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen.nchildren[0]) == SLDisplayable
    assert expected == str(decompressed[0].block[0].screen.nchildren[0])

def test_parse_sl_displayable_imagebutton_statement():
    """
    screen test:
        imagebutton auto "test_%s.png" action Exit() <- this is our target block
    """
    expected = 'imagebutton auto "test_%s.png" action Exit()'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_displayable_as_imagebutton.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen.nchildren[0]) == SLDisplayable
    assert expected == str(decompressed[0].block[0].screen.nchildren[0])

def test_parse_sl_displayable_textbutton_statement():
    """
    screen test:
        textbutton "test" action Exit() <- this is our target block
    """
    expected = 'textbutton "test" action Exit()'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_displayable_as_textbutton.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen.nchildren[0]) == SLDisplayable
    assert expected == str(decompressed[0].block[0].screen.nchildren[0])

def test_parse_sl_displayable_style_statement():
    """
    screen test:
        vbox: <- this is our target block
            add "test.png"
            add "test.png"
    """
    expected_children = ['add "test.png"', 'add "test.png"', '']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_displayable_as_style.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen.nchildren[0]) == SLDisplayable
    assert str(decompressed[0].block[0].screen.nchildren[0]) == 'vbox:'
    assert expected_children == list(map(str, decompressed[0].block[0].screen.nchildren[0].nchildren))

def test_parse_sl_displayable_style_in_frame_statement():
    """
    screen test:
        frame:
            vbox: <- this is our target block
                add "test.png"
                add "test.png"
    """
    expected_children = ['add "test.png"', 'add "test.png"', '']

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_displayable_as_style_in_frame.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen.nchildren[0]) == SLDisplayable
    assert type(decompressed[0].block[0].screen.nchildren[0].nchildren[0]) == SLDisplayable
    assert str(decompressed[0].block[0].screen.nchildren[0].nchildren[0]) == 'vbox:'
    assert expected_children == list(map(str, decompressed[0].block[0].screen.nchildren[0].nchildren[0].nchildren))

def test_parse_sl_displayable_dismiss_statement():
    """
    screen test:
        dismiss action Return() <- this is our target block
    """
    expected = 'dismiss action Return()'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_displayable_as_dismiss.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen.nchildren[0]) == SLDisplayable
    assert expected == str(decompressed[0].block[0].screen.nchildren[0])

def test_parse_sl_displayable_on_statement():
    """
    screen test:
        on "show" action Return() <- this is our target block
    """
    expected = 'on "show" action Return()'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_displayable_as_on.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen.nchildren[0]) == SLDisplayable
    assert expected == str(decompressed[0].block[0].screen.nchildren[0])

def test_parse_sl_displayable_timer_statement():
    """
    screen test:
        timer 3.0 action Return() <- this is our target block
    """
    expected = 'timer 3.0 action Return()'

    decompressed = pickle.loads(loader.load_file(os.path.join(os.path.dirname(__file__), 'test_sl_displayable_as_timer.rpyc')))[1]

    assert type(decompressed[0]) == Init
    assert type(decompressed[0].block[0]) == Screen
    assert type(decompressed[0].block[0].screen.nchildren[0]) == SLDisplayable
    assert expected == str(decompressed[0].block[0].screen.nchildren[0])
