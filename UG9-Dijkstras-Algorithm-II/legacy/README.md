# Preserved historical matrix source

`Main.java` retains the exact pre-repair working-file bytes, including CRLF
line endings: SHA-256 `ca5e56778c33f9990d8c92e749d0a3698895943f4353c37908f766f0bf76aaaf`.
Git previously stored normalized LF bytes with SHA-256
`c1a2f29a637080257e70aa751a12c4d3457d46e7916160885f7e58fb4c8ac8d1`.
Its path-specific Git attribute preserves this snapshot without conversion.

This historical program overwrites parallel weights, uses overflowing int
distances/queue comparisons, prints misleading unreachable output and claims
an incorrect complexity. Retain it for comparison and use the maintained
roles for assignments. It is excluded from role imports and active counts.
