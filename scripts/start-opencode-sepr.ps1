$ErrorActionPreference = "Stop"

$repo = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repo

$env:OPENCODE_DISABLE_CLAUDE_CODE_PROMPT = "1"
$env:OPENCODE_ENABLE_EXA = "1"

opencode @args
