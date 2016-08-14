Python debugging tips and tricks
================================
https://slides.com/invisibleroads/debugging-tips

- Triple exclamation marks (!!!) indicate essential techniques.
- Installation instructions are specific to Fedora. Other Linux distributions have equivalent commands. OS X users should use the [brew package manager](http://brew.sh/). Windows users may find it easier to install a prepackaged solution such as [Anaconda](https://store.continuum.io/cshop/anaconda/) or [Python(x,y)](http://python-xy.github.io/).



Run commands
------------
Here are some [keyboard shortcuts that can save you time in the Bash command shell](http://www.howtogeek.com/howto/ubuntu/keyboard-shortcuts-for-bash-command-shell-for-ubuntu-debian-suse-redhat-linux-etc/).

    CTRL-w  # Delete word before cursor
    ALT-d   # Delete word after cursor

    ALT-f   # Move one word forward
    ALT-b   # Move one word backward

    CTRL-u  # Clear line before cursor
    CTRL-k  # Clear line after cursor
    CTRL-l  # Clear screen

    CTRL-r  # Search commands backward
    CTRL-s  # Search commands forward

    TAB     # Autocomplete paths

You can also set vi editing mode!

    set -o vi



Isolate development packages from system packages
-------------------------------------------------
Keep development packages separate from system packages to prevent conflicts using [virtualenv](https://virtualenv.pypa.io/en/latest/) and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/).

    # Install setuptools
    wget https://bootstrap.pypa.io/ez_setup.py -O /tmp/ez_setup.py
    sudo python /tmp/ez_setup.py
    # Install pip
    sudo easy_install pip
    # Install virtualenvwrapper
    sudo pip install -U virtualenvwrapper

    export WORKON_HOME=~/.virtualenvs
    source virtualenvwrapper.sh
    # Prepare virtual environment
    mkvirtualenv crosscompute
    # Activate virtual environment
    workon crosscompute

    # Use shortcuts
    cdvirtualenv
    cdsitepackages pip



Prototype code
--------------
Run multiple terminals with minimal screen clutter using [tmux](http://www.openbsd.org/cgi-bin/man.cgi/OpenBSD-current/man1/tmux.1).

    # Install tmux
    sudo dnf -y install tmux
    # Configure tmux
    vim ~/.tmux.conf
        # Turn off status bar
        set -g status off
        # Change key binding from default CTRL-b to CTRL-a
        set-option -g prefix C-a
    # Run multiple terminals
    tmux
        CTRL-a c        # Open new
        CTRL-a n        # Switch to next
        CTRL-a p        # Switch to previous
        CTRL-a ;        # Switch back

        CTRL-a [        # Start copy mode to view terminal history using vim keys
            ?           # Search backward
            /           # Search forward
            gg          # Go to start
            SPACE       # Start selection
            G           # Go to end
            ENTER       # End selection
            q           # Quit copy mode
        CTRL-a ]        # Paste selection from copy mode

        CTRL-a "        # Split into top and bottom
        CTRL-a %        # Split into left and right
        CTRL-a d        # !!! Detach
    tmux list-sessions  # List sessions
    tmux ls             # List sessions
    tmux attach         # !!! Attach session
    tmux attach -t 0    # Attach session 0

Experiment incrementally using [jupyter](https://jupyter.org/).

    # Install jupyter
    source ~/.virtualenvs/crosscompute/bin/activate
    pip install -U jupyter ipython pyzmq tornado
    # Install optional packages
    pip install -U matplotlib
    # Start jupyter (see prototype-bits.ipynb)
    jupyter notebook
        %debug  # !!! Enter debugger after an exception
        %%capture interesting_output
        %%writefile useful-code.py



Convert prototype into a script
-------------------------------
!!! Update .vimrc (see https://github.com/invisibleroads/scripts/blob/master/.vimrc for an example configuration).

    vim .vimrc
        set tabstop=4      " Convert existing tabs to 4 spaces
        set shiftwidth=4   " Use >> and << to shift indent by 4 columns
        set softtabstop=4  " Insert/delete 4 spaces with TAB/BACKSPACE
        set expandtab      " Insert spaces when hitting TAB
        set shiftround     " Round indent to multiple of shiftwidth
        set autoindent     " Align new line indent with previous line

!!! Install [vundle](https://github.com/gmarik/Vundle.vim) to manage plugins (see http://unlogic.co.uk/2013/02/08/vim-as-a-python-ide/).

    git clone --depth=1 https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim
    vim .vimrc
        set nocompatible
        filetype off
        set rtp+=~/.vim/bundle/Vundle.vim
        call vundle#begin()
        Plugin 'gmarik/Vundle.vim'
        " Specify bundles here
        call vundle#end()
        filetype plugin indent on
        " Configure settings here
    vim
        :PluginList

!!! Install [syntastic](https://github.com/scrooloose/syntastic) to check syntax on save.

    vim .vimrc
        Plugin 'scrooloose/syntastic'
            set statusline+=%#warningmsg#
            set statusline+=%{SyntasticStatuslineFlag()}
            set statusline+=%*
            let g:syntastic_auto_loc_list=1
            let g:syntastic_check_on_wq = 0
            let g:syntastic_loc_list_height=3
    vim +PluginInstall +qall now
    source ~/.virtualenvs/crosscompute/bin/activate
    pip install -U flake8

Install [jedi-vim](https://github.com/davidhalter/jedi-vim) for autocompletion with CTRL-SPACE and documentation with K.

    vim .vimrc
        Plugin 'davidhalter/jedi-vim'
            let g:jedi#popup_on_dot = 0
            let g:jedi#show_call_signatures = 0
    vim +PluginInstall +qall now
    source ~/.virtualenvs/crosscompute/bin/activate
    pip install -U jedi

Choose other plugins.

- [delimitMate](https://github.com/Raimondi/delimitMate) gives smart quotes, parentheses, brackets.
- [vim-airline](https://github.com/bling/vim-airline) provides an informative status bar.
- [SimpylFold](https://github.com/tmhedberg/SimpylFold) folds code.
- [ctrlp](https://github.com/ctrlpvim/ctrlp.vim) locates a file by name.
- [dirdiff](https://github.com/will133/vim-dirdiff) locates a file by name.

Paste into a graphical terminal while preserving indents with CTRL-SHIFT-V.

    vim
        :set paste
        :set nopaste

Use basic autocompletion (does not require jedi).

    vim
        CTRL-n
        CTRL-p



Debug script
------------
When debugging, you can either set an explicit breakpoint or launch the script through the debugger. With the exception of IPython, the pdb variants share the same keyboard shortcuts.

- [ipython](http://ipython.org/ipython-doc/stable/interactive/index.html)
- [pudb](https://pypi.python.org/pypi/pudb)
- [wdb](https://pypi.python.org/pypi/wdb)
- [ipdb](https://pypi.python.org/pypi/ipdb)

Install packages.

    source ~/.virtualenvs/crosscompute/bin/activate
    pip install -U ipython pudb wdb ipdb

!!! Set breakpoints.

    import IPython; IPython.embed()           # !!! Explore environment
    import pudb; pudb.set_trace()             # !!! Revive Turbo Debugger
    import wdb; wdb.set_trace()               # Debug remotely for threads
    import ipdb; ipdb.set_trace()             # Step through code with ipython

Use two debuggers in tandem.

    import IPython; IPython.embed()
    import pudb; pudb.set_trace()

Use [ipython](http://ipython.org/ipython-doc/stable/interactive/index.html).

    pdb    # !!! Toggle debugger on exception
    debug  # !!! Start debugger on most recent exception

    whos   # !!! List variables in namespace
    pwd    # Show present working directory

    paste  # Paste clipboard contents
    prun   # Profile code to identify bottlenecks

    save   # Save commands to file
    store  # Store variables for another session

!!! Run script with arguments (--), drop into [ipdb](https://pypi.python.org/pypi/ipdb) on exception (--pdb), drop into [ipython](https://pypi.python.org/pypi/ipython) on completion (-i).

    ipython --pdb -i -- print-lines.py quote1.txt

!!! Step through script with arguments (--) with [pudb](https://pypi.python.org/pypi/pudb).

    pudb -- explore-values.py arg1 arg2
        n               # !!! Execute next line
        s               # !!! Step into function
        CTRL-x          # Execute custom code
        qq              # Quit

Trace on CTRL-C.

    import pudb; pudb.set_interrupt_handler()

Debug threads or Docker containers.

    import wdb; wdb.set_trace()



Debug test
----------
Testing is easy with [pytest](http://pytest.org/latest/getting-started.html#getstarted), but it only supports the default debugger, which you can extend with [pdb++](https://bitbucket.org/antocuni/pdb/src).

- [pytest](http://pytest.org/latest/getting-started.html#getstarted)
- [pdb++](https://pypi.python.org/pypi/pdbpp/)

Install packages. The pdbpp package enhances pdb and is compatible with pytest.

    source ~/.virtualenvs/crosscompute/bin/activate
    pip install -U pytest pdbpp

Invoke debugger when a test fails.

    py.test --pdb

Set breakpoints in test.

    import pdb; pdb.set_trace()



Maintain logs during production
-------------------------------
Define a namespaced [logger](https://docs.python.org/2/library/logging.html) for the module.

    import logging

    logger = logging.getLogger(__name__)
    logger.addHandler(logging.NullHandler())

    logger.debug('a')
    logger.info('b')
    logger.warning('c')
    logger.error('d')
    logger.critical('e')

Specify which loggers to expose in the main script. For example, if your submodules are xyz.abc and xyz.def then you can use logging.getLogger('xyz') to listen to both submodules.

    import logging
    logging.getLogger('xyz').setLevel(logging.INFO)
    logging.basicConfig()

Use [traceback](https://docs.python.org/2/library/traceback.html) to capture unexpected exceptions.

    import logging
    import traceback
    try:
        {}[0]
    except Exception:
        logging.error(traceback.format_exc())

Configure a [rsyslog server](https://hynek.me/articles/taking-some-pain-out-of-python-logging/) to centralize logs across multiple processes.
