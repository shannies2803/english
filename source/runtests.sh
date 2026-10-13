#!/bin/sh
# Every browser test, in one command. Run after any change to build_site2.py.
#
# Three things have to be true before a suite counts as a pass:
#   1. node exited 0 — a suite that crashed before launching a browser is not a pass.
#      (This was a real bug: a missing node_modules made all 14 suites crash, and the
#      old grep-only runner reported "all browser tests pass".)
#   2. the output is not a stack trace or an unhandled rejection.
#   3. the output contains none of the failure patterns below.
# Patterns are case-sensitive on purpose: "clipped tabs: none" must not match.
fail=0
for t in smoke smoke2 smoke3 smoke4 smoke6 smoke7 smoke8 marktest marktest2 marktest3 marktest4 datatest widths navcheck contrast subjects; do
  [ -f "$t.mjs" ] || continue
  out=$(node "$t.mjs" 2>&1); rc=$?
  if [ $rc -ne 0 ]; then
    echo "CRASH $t (exit $rc)"
    echo "$out" | head -4 | sed 's/^/      /'
    fail=1
    continue
  fi
  if echo "$out" | grep -qE "Error \[ERR_|Cannot find (package|module)|UnhandledPromiseRejection|^ *at [A-Za-z_$]|Traceback"; then
    echo "CRASH $t (stack trace in output)"
    echo "$out" | grep -E "Error \[ERR_|Cannot find (package|module)|UnhandledPromiseRejection" | head -2 | sed 's/^/      /'
    fail=1
    continue
  fi
  if [ "$(echo "$out" | wc -l)" -lt 2 ]; then
    echo "CRASH $t (no output — did it run?)"
    fail=1
    continue
  fi
  if echo "$out" | grep -qE "FAIL|STATE LOST|LOST OR CHANGED|pageerror|ERRORS: \[|marker: [1-9]|misleading\): [1-9]|overlap true|clipped tabs: [^n]"; then
    echo "FAIL  $t"
    echo "$out" | grep -E "FAIL|LOST|ERRORS|marker:|misleading|overlap true|clipped tabs: [^n]" | head -4
    fail=1
  else
    echo "pass  $t"
  fi
done
[ $fail -eq 0 ] && printf '\nall browser tests pass\n'
exit $fail
