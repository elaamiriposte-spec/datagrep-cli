#compdef datagrep
# Zsh completion for datagrep
# Installation: cp datagrep.zsh /usr/share/zsh/site-functions/_datagrep
# Or: cp datagrep.zsh ~/.zsh/completions/_datagrep

_datagrep() {
    local -a args modes formats opts
    
    modes=('contains' 'exact' 'startswith' 'endswith' 'regex')
    formats=('auto' 'csv' 'json' 'xlsx')
    output_formats=('csv' 'json' 'table' 'raw')
    
    args=(
        '1:input file:_files'
        '2:columns:' 
        '3:value:'
        '(--help --version)--version[Show version and exit]'
        '(--help)--help[Show help message]'
        '--input-format=[Input format]:format:(auto csv json xlsx)'
        '--mode=[Search mode]:mode:(contains exact startswith endswith regex)'
        '(-i --ignore-case)'{-i,--ignore-case}'[Ignore case sensitivity]'
        '(-d --delimiter)'{-d,--delimiter}'=[CSV delimiter]:delimiter:'
        '--encoding=[File encoding]:encoding:(utf-8 latin-1 ascii)'
        '--output-format=[Output format]:format:(csv json table raw)'
        '(-s --select)'{-s,--select}'=[Select columns]:columns:'
        '(-o --output)'{-o,--output}'=[Output file]:file:_files'
        '(-n --limit)'{-n,--limit}'=[Max results]:limit:'
        '--sort=[Sort column]:column:column:order'
        '--where=[Filter condition]:condition:'
        '--count[Count matching records only]'
        '--config=[Config file]:file:_files'
        '--color[Colorize output]'
        '--progress[Show progress bar]'
        '--preview=[Preview N rows]:rows:'
        '--sample=[Show sample N rows]:rows:'
        '(-v --verbose)'{-v,--verbose}'[Verbose output]'
        '--debug[Debug output]'
        '--describe[Show schema only]'
    )
    
    _arguments -s -S "$args[@]"
}

_datagrep
