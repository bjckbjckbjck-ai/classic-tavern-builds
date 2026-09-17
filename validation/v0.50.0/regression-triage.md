# v0.50 regression triage

## Default headless regression

- Original complete run: `.runtime/v50-verify.log`, 96 suites, 95 OK and only `audit_v45_test` failed; 2287 passing assertions.
- Original audit log: `.runtime/v390-audit_v45_test.log`, 19 UI PASS and 2 UI FAIL.
- Cause: the old UI tour treated one trinket click as purchase. Current trinket UI intentionally selects first and purchases only after clicking `TrinketConfirm`.
- Test-only correction: preserve actual pointer dispatch and purchase assertions, add both confirmation clicks, add two assertions that first click leaves coins and owned trinkets unchanged, strengthen greater choice assertion to two equipped trinkets.
- Fresh headless audit run: `.runtime/v50-triage-audit_v45_test.log`, exit 0, 23 UI PASS, no FAIL, SCRIPT ERROR or ERROR.
- Combined coverage: the 96 suites all pass across the full run and the corrected targeted rerun, 2291 passing assertions. This is not a claim of a second complete clean run.

## Built-in network smoke state machine

- Before-change probe: `.runtime/v50-network-before-host.log` and `.runtime/v50-network-before-client.log`.
- Client received recruit serial 1, sent buy/play/buy_spell/cast/ready in the same frame, then received serial 2 with one hand card and no board/spell casts/ready. Notice: `操作或目标已变化，请重新选择`.
- Root cause: all five intents used the initial action guard. Buying changes the authoritative serial and hand UID; the four remaining guards are correctly rejected. Host timed out. This is an obsolete test harness, not a production permission failure.
- Only `main.gd` test variables and test helper/tick paths changed. Each action now waits for a newer authoritative serial, locates the exact purchased UID, validates its move into hand/board, then sends the next guarded request. Host smoke fixture uses micro plus banana. Ordinary game rules and requests remain unchanged.
- `python scripts/network_smoke.py` source headless two-process rerun: exit 0, real buy/play/buy_spell/cast/ready, nonempty combat replay, private snapshots and disconnect BOT takeover passed. Evidence: `.runtime/v50-source-network-after.log` and `.runtime/v21-network-{host,client}.log`.
- Host shutdown emitted ObjectDB instances leaked and 1 resource still in use. All required network checks passed, but the first source run is not a clean shutdown-log result.
- Remote entry point rerun against a local dedicated process: `python .runtime/v50_remote_network_after.py`, exit 0, buy/play/ready and combat passed. Evidence `.runtime/v50-remote-after-remote.log`; server `.runtime/v50-remote-after-server.log`. No SCRIPT ERROR or ERROR in remote client output.
- `git diff --check -- scripts/main.gd tests/audit_v45_test.gd`: exit 0 (only Git CRLF normalization warnings).

Release follow-up: EXE/APK were regenerated after this test-harness change. The final EXE native two-process smoke passed with both exit codes 0 and clean logs; the final APK was installed and exercised on the host-GPU Android emulator. See README.md, network-results.json and installed-apk.json.
