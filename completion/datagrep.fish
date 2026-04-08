#!/usr/bin/env fish
# Fish completion for datagrep
# Installation: cp datagrep.fish ~/.config/fish/completions/datagrep.fish

# Main command
complete -c datagrep -f -d "Search CSV, JSON, or Excel records"

# Version and help
complete -c datagrep -l version -d "Show version and exit"
complete -c datagrep -l help -d "Show help message"

# Positional arguments
complete -c datagrep -n "__fish_is_nth_arg 1" -xa "(__fish_complete_suffix '.csv;.json;.xlsx')" -d "Input file"
complete -c datagrep -n "__fish_is_nth_arg 2" -x -d "Columns to search"
complete -c datagrep -n "__fish_is_nth_arg 3" -x -d "Search value"

# Input/Output options
complete -c datagrep -l input-format -x -a "auto csv json xlsx" -d "Input format"
complete -c datagrep -l output-format -x -a "csv json table raw" -d "Output format"
complete -c datagrep -l output -s o -r -d "Output file"

# Search options
complete -c datagrep -l mode -x -a "contains exact startswith endswith regex" -d "Search mode"
complete -c datagrep -l ignore-case -s i -d "Ignore case sensitivity"
complete -c datagrep -l where -x -d "Filter condition"
complete -c datagrep -l sort -x -d "Sort by column"

# Display options
complete -c datagrep -l select -s s -x -d "Select columns"
complete -c datagrep -l limit -s n -x -d "Limit results"
complete -c datagrep -l preview -x -d "Preview N rows"
complete -c datagrep -l sample -x -d "Show N sample rows"

# Format options
complete -c datagrep -l delimiter -s d -x -d "CSV delimiter"
complete -c datagrep -l encoding -x -a "utf-8 latin-1 ascii" -d "File encoding"

# Special modes
complete -c datagrep -l count -d "Count matching records only"
complete -c datagrep -l describe -d "Show schema only"
complete -c datagrep -l config -r -d "Configuration file"

# Display options
complete -c datagrep -l color -d "Colorize output"
complete -c datagrep -l progress -d "Show progress bar"
complete -c datagrep -l verbose -s v -d "Verbose output"
complete -c datagrep -l debug -d "Debug output"
