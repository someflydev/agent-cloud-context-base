# No Default Credentials

Cloud examples must not rely on ambient default credentials unless the operator
has explicitly selected that test lane.

The failure mode is accidental access to a real account, project, subscription,
or tenant while a developer expected a local emulator or isolated test stack.
Default credentials also make reproduction difficult because success depends on
the person who ran the command.

Prefer named profiles, workload identities, emulator endpoints, or short-lived
test credentials. Document the required credential source beside the verification
command and keep dev and test credential paths separate.

When this policy fails, replace ambient credential reads with explicit
environment variables or provider config for the intended lane.
