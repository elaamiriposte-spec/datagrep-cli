#!/bin/bash
# Bash completion script for datagrep
# Installation: sudo cp datagrep.bash /usr/share/bash-completion/completions/datagrep
# Or: cp datagrep.bash ~/.bash_completion.d/datagrep

_datagrep_completions() {
    local cur prev words cword
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # All available options
    local opts="--help --version --input-format --mode --ignore-case --delimiter --encoding --output-format --select --output --limit --sort --where --count --config --color --progress --preview --sample --verbose --debug --describe"
    
    # Options that take arguments
    local args_opts="--input-format --mode --delimiter --encoding --output-format --select --output --limit --sort --where --config --preview --sample"
    
    # Complete options
    if [[ "$cur" == -* ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
    
    # Complete option arguments
    case "$prev" in
        --input-format)
            COMPREPLY=( $(compgen -W "auto csv json xlsx" -- ${cur}) )
            return 0
            ;;
        --mode)
            COMPREPLY=( $(compgen -W "contains exact startswith endswith regex" -- ${cur}) )
            return 0
            ;;
        --output-format)
            COMPREPLY=( $(compgen -W "csv json table raw" -- ${cur}) )
            return 0
            ;;
        --output|--config)
            COMPREPLY=( $(compgen -f -- ${cur}) )
            return 0
            ;;
        --delimiter|--encoding|--select|--limit|--sort|--where|--preview|--sample)
            # These take argument values
            return 0
            ;;
    esac
    
    # Complete first positional argument (input file)
    if [[ ${COMP_CWORD} -eq 1 ]] ; then
        COMPREPLY=( $(compgen -f -- ${cur}) )
        return 0
    fi
}

complete -o bashdefault -o default -o filenames -F _datagrep_completions datagrep
