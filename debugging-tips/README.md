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


Use tmux
Use ipython notebook
    pylab
    ipython notebook --debug
    select text and type quote or bracket or parenthesis



Convert prototype into a script
-------------------------------
Use vim > syntastic
Use vim > delimitMate
Use vim > ctrlp.vim
Use vimrc
Use :set paste
CTRL-SHIFT-V
`` to go to last location
Use :set nopaste
Incorporate http://unlogic.co.uk/2013/02/08/vim-as-a-python-ide/
Incorporate http://docs.python-guide.org/en/latest/dev/env/
Incorporate https://github.com/mbrochh/vim-as-a-python-ide



Debug script
------------
Use IPython.embed()
    Use pdb magic command in IPython
    Use timeit
    Use prun
    Use x<TAB>
    Use x.<TAB>
    Use x?
    Use x??
    cd
    pwd
    whos
    ls
    debug
    paste
    save
    store
Use ipdb.set_trace()
Use pudb.set_trace()

Use ipython -i --pdb --debug --
Use ipython -i --pydb --debug --



Maintain logs during production
-------------------------------
Use logging
Use traceback
Setup logging server with pyzmq
