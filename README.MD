<div align="center">
    <h1>Ren'Py Cracken</h1>
</div>
<p>Ren'Py Cracken is a Python project that can reconstruct your .rpyc\.rpa files to its (mostly) original form.</p>
<h2>Features</h2>
<ul>
    <li>
        <b>Multiple sources handling</b>
        <p>
            This project is able to handle both .rpyc and .rpa files one by one or grouped in folders.
        </p>
    </li>
    <li>
        <b>Recursive search</b>
        <p>
            If there are .rpyc inside of an archive file, renpy-cracken could handle them as well.
        </p>
    </li>
    <li>
        <b>Python code prettifier</b>
        <p>
            If you want, renpy-cracken could make your Python code snippets more pretty (fix formating and indent, remove accessive empty lines, etc.)
        </p>
    </li>
</ul>
<h2>Installation</h2>
<p>
    <h3>GUI</h3>
    Here is a <a href="https://github.com/dododo25/renpy-cracken/releases">link</a> to the latest version of executable files.
</p>
<p>
    <h3>Console</h3>
    <ol>
        <li>
            Download the latest version of Python 3.14 or higher from <a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a> and install it.
        </li>
        <li>
            Download the latest version of <a href="https://www.python.org/downloads/">renpy-cracken</a> and unzip somewhere on your computer.
        </li>
        <li>
            <span>
            Using the termial, go to the folder where this project is located and then type:
            </span>
            <pre>
python -m venv venv
venv/Scripts/activate (on Windows)
. venv/bin/activate (on Linux\Mac)
pip install .</pre>
        </li>
        <li>
            To verify that everything works correctly, type:
            <code>python src/cracken.py --help</code>
        </li>
    </ol>
</p>

If you have any other questions or suggestions, please leave them on "<a href="https://github.com/dododo25/renpy-cracken/issues">Issues</a>" page.

That's it. Hope you'll enjoy 🐦