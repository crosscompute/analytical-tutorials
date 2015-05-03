Python debugging tips and tricks
================================



Isolate development packages from system packages
-------------------------------------------------
Keep development packages separate from system packages to prevent conflicts.

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



Prototype code
--------------
Run multiple terminals with minimal screen clutter.

    # Install tmux
    sudo yum -y install tmux
    # Configure tmux
    vim .tmux.conf
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
        CTRL-a d        # Detach
    tmux list-sessions  # List sessions
    tmux attach         # Attach session
    tmux attach -t 0    # Attach session 0

Experiment incrementally.

    # Install ipython notebook
    source ~/.virtualenvs/crosscompute/bin/activate
    pip install -U ipython pyzmq tornado
    # Install optional packages
    pip install -U matplotlib
    # Start ipython notebook (see prototype-bits.ipynb)
    ipython notebook
        %%capture interesting_output
        %%writefile useful-code.py



Convert prototype into a script
-------------------------------
Update .vimrc (see https://github.com/invisibleroads/scripts/blob/master/.vimrc).

    vim .vimrc
        set tabstop=4      " Convert existing tabs to 4 spaces
        set shiftwidth=4   " Use >> and << to shift indent by 4 columns
        set softtabstop=4  " Insert/delete 4 spaces with TAB/BACKSPACE
        set expandtab      " Insert spaces when hitting TAB
        set shiftround     " Round indent to multiple of shiftwidth
        set autoindent     " Align new line indent with previous line

Install vundle to manage plugins (see http://unlogic.co.uk/2013/02/08/vim-as-a-python-ide/).

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

Install [syntastic](https://github.com/scrooloose/syntastic) to check syntax on save.

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

Install [jedi-vim](https://github.com/davidhalter/jedi-vim) for autocompletion with \<CTRL-SPACE\>.

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

Paste into a graphical terminal while preserving indents with \<CTRL-SHIFT-V\>.

    vim
        :set paste
        :set nopaste

Use basic autocompletion (does not require jedi).

    vim
        <CTRL-n>
        <CTRL-p>



Debug script
------------
Install packages.

    source ~/.virtualenvs/crosscompute/bin/activate
    pip install -U trepan ipdb bpython pudb

Set breakpoints.

    import IPython; IPython.embed()         # Explore breakpoint environment
    import trepan.api; trepan.api.debug()   # Step through code with extra features
    import ipdb; ipdb.set_trace()           # Step through code with ipython
    import bpdb; bpdb.set_trace()           # Step through code with bpython
    import pudb; pudb.set_trace()           # Revive Borland Turbo Debugger

Use ipython.

    pdb    # Toggle debugger on exception
    debug  # Start debugger on most recent exception

    whos   # List variables in namespace
    pwd    # Show present working directory

    paste  # Past clipboard contents
    prun   # Profile code to identify bottlenecks

    save   # Save commands to file
    store  # Store variables for another session

Run script with arguments (--), drop into ipdb on exception (--pdb), drop into ipython on completion (-i).

    ipython --pdb -i -- print-lines.py quote1.txt

Step through script with arguments (--).

    trepan2 -- print-lines.py quote2.txt
        b 7             # Set breakpoint at line 7
        c               # Run until breakpoint
        display line    # Set watch
        n               # Execute next line
        n               # Execute next line
        info threads    # Show threads



Maintain logs during production
-------------------------------
Use logging.

    import logging

    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.basicConfig(level=logging.DEBUG)

    logging.debug('a')
    logging.info('b')
    logging.warning('c')
    logging.error('d')
    logging.critical('e')

Use traceback to capture unexpected exceptions.

    import logging
    import traceback
    try:
        {}[0]
    except Exception:
        exception_text = traceback.format_exc()
        logging.error(exception_text)

Setup logging server with pyzmq to debug microservices (see https://zeromq.github.io/pyzmq/logging.html).
