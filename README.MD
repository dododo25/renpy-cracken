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
    Go to this page <a href="https://github.com/dododo25/renpy-cracken/releases">https://github.com/dododo25/renpy-cracken/releases</a> and download the latest version.
</p>
<p>
    <h3>Console</h3>
    <ol>
        <li>
            Download the latest version of Python 3 from <a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a> and install it.
        </li>
        <li>
            Download the latest version of renpy-cracken (<a href="https://www.python.org/downloads/">https://github.com/dododo25/renpy-cracken/archive/refs/heads/main.zip</a>) and unzip somewhere on your computer.
        </li>
        <li>
            <span>
            Using the termial, go to the folder where this project is located and then type:
            </span>
            <p>
                <code>python -m venv venv</code>
            </p>
            <p>
                <code>venv\Scripts\activate</code> on Windows or
                <code>venv\bin\activate</code> on Linux\Mac
            </p>
            <p>
                <code>pip install -f requirements.txt</code>
            </p>
            <p>
                <code>python console\main.py --help</code>
            </p>
        </li>
    </ol>
</p>

If you have any othe questions, please leave them <a href="https://github.com/dododo25/renpy-cracken/issues">here</a>.

That's it. Hope you enjoy 🐦