# PowerShell completion for datagrep
# Installation: Copy to $PROFILE and reload PowerShell

$scriptblock = {
    param($wordToComplete, $commandAst, $cursorPosition)
    
    $options = @(
        '--version'
        '--help'
        '--input-format'
        '--mode'
        '--ignore-case'
        '--delimiter'
        '--encoding'
        '--output-format'
        '--select'
        '--output'
        '--limit'
        '--sort'
        '--where'
        '--count'
        '--config'
        '--color'
        '--progress'
        '--preview'
        '--sample'
        '--verbose'
        '--debug'
        '--describe'
    )
    
    $modes = @('contains', 'exact', 'startswith', 'endswith', 'regex')
    $formats = @('auto', 'csv', 'json', 'xlsx')
    $output_formats = @('csv', 'json', 'table', 'raw')
    
    # Get the last option
    $lastOption = $commandAst.CommandElements | Select-Object -Last 1 | ForEach-Object { $_.Value }
    
    # Provide completions based on context
    if ($lastOption -eq '--input-format') {
        $formats | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object {
            [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
        }
    } elseif ($lastOption -eq '--mode') {
        $modes | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object {
            [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
        }
    } elseif ($lastOption -eq '--output-format') {
        $output_formats | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object {
            [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
        }
    } elseif ($lastOption -eq '--encoding') {
        @('utf-8', 'latin-1', 'ascii') | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object {
            [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
        }
    } else {
        # Regular option completion
        $options | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object {
            [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
        }
    }
}

Register-ArgumentCompleter -CommandName datagrep -ScriptBlock $scriptblock
