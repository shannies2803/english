#!/bin/sh
# Every browser test, in one command. Run after any change to build_site2.py.
# Patterns are case-sensitive on purpose: "clipped tabs: none" must not match.
fail=0
for t in smoke smoke2 smoke3 smoke4 smoke6 smoke7 smoke8 marktest marktest2 marktest3 marktest4 datatest widths navcheck; do
  [ -f "$t.mjs" ] || continue
  out=$(node "$t.mjs" 2>&1)
  if echo "$out" | grep -qE "FAIL|STATE LOST|LOST OR CHANGED|pageerror|ERRORS: \[|marker: [1-9]|misleading\): [1-9]|overlap true|clipped tabs: [^n]"; then
    echo "FAIL  $t"
    echo "$out" | grep -E "FAIL|LOST|ERRORS|marker:|misleading|overlap true|clipped tabs: [^n]" | head -4
    fail=1
  else
    echo "pass  $t"
  fi
done
[ $fail -eq 0 ] && echo "\nall browser tests pass"
exit $fail
