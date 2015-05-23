Python debugging tips and tricks
================================
http://bit.ly/pdbtips

- Triple exclamation marks (!!!) indicate essential techniques.
- Installation instructions are specific to Fedora. Other Linux distributions have equivalent commands.
- Mac OS X and Windows users may find it easier to install a prepackaged solution such as Anaconda.



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
    sudo yum -y install tmux
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

Experiment incrementally using [ipython notebook](http://ipython.org/notebook.html).

    # Install ipython notebook
    source ~/.virtualenvs/crosscompute/bin/activate
    pip install -U ipython pyzmq tornado
    # Install optional packages
    pip install -U matplotlib
    # Start ipython notebook (see prototype-bits.ipynb)
    ipython notebook
        debug  # !!! Enter debugger after an exception
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
- [vim-surround](https://github.com/tpope/vim-surround) surrounds text with delimiters or tags
- [vim-repeat](https://github.com/tpope/vim-repeat) repeats plugin actions (such as vim-surround).
- [SimpylFold](https://github.com/tmhedberg/SimpylFold) folds code.
- [vim-fugitive](https://github.com/tpope/vim-fugitive) integrates with git.
- [vim-airline](https://github.com/bling/vim-airline) provides an informative status bar.
- [ctrlp](https://github.com/kien/ctrlp.vim) locates a file by name.

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
- [ipdb](https://pypi.python.org/pypi/ipdb)
- [bpdb](http://docs.bpython-interpreter.org/bpdb.html)
- [trepan](https://github.com/rocky/python2-trepan/wiki/Tutorial)
- [pdb++](https://bitbucket.org/antocuni/pdb/src)

Install packages.

    source ~/.virtualenvs/crosscompute/bin/activate
    pip install -U trepan ipdb bpython pudb pdbpp

!!! Set breakpoints.

    import IPython; IPython.embed()         # !!! Explore breakpoint environment
    import pudb; pudb.set_trace()           # !!! Revive Borland Turbo Debugger
    import ipdb; ipdb.set_trace()           # Step through code with ipython
    import bpdb; bpdb.set_trace()           # Step through code with bpython
    import trepan.api; trepan.api.debug()   # Step through code with extra features

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

    pudb -- explore-values.py
        n               # !!! Execute next line
        s               # !!! Step into function
        CTRL-x          # Execute custom code
        qq              # Quit

Step through script with arguments (--) with [trepan](https://pypi.python.org/pypi/trepan).

    trepan2 -- print-lines.py quote2.txt
        b 7             # !!! Set breakpoint at line 7
        c               # !!! Run until breakpoint
        display line    # Set watch
        1 + 1           # Execute custom code
        n               # Execute next line
        n               # Execute next line
        info threads    # Show threads



Debug test
----------
Invoke debugger when a test fails.

    py.test --pdb

Set breakpoints in test.

    import IPython; IPython.embed()
    import pudb; pudb.set_trace()



Maintain logs during production
-------------------------------
Use [logging](https://docs.python.org/2/library/logging.html).

    import logging

    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.basicConfig(level=logging.DEBUG)

    logging.debug('a')
    logging.info('b')
    logging.warning('c')
    logging.error('d')
    logging.critical('e')

Use [traceback](https://docs.python.org/2/library/traceback.html) to capture unexpected exceptions.

    import logging
    import traceback
    try:
        {}[0]
    except Exception:
        exception_text = traceback.format_exc()
        logging.error(exception_text)

Setup logging server with [pyzmq](https://pypi.python.org/pypi/pyzmq) to debug microservices (see https://zeromq.github.io/pyzmq/logging.html).
