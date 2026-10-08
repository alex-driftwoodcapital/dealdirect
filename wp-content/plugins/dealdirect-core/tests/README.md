# dealdirect-core tests

- `php tests/run.php`: unit tests for `DealDirect\Submission` (validation, HubSpot value mapping, payload). No WordPress needed.
- `tests/rest-integration.php`: end-to-end REST checks (nonce, honeypot, accreditation refusal, offering-request lookup, One to One retry, rate limit) against a **local** WordPress with HubSpot faked through `pre_http_request`. Install `tests/scf-stub.php` as `wp-content/plugins/secure-custom-fields/secure-custom-fields.php`, activate both plugins, then `wp eval-file wp-content/plugins/dealdirect-core/tests/rest-integration.php`. The "Cannot modify header information" warnings come from `setcookie` after CLI output and do not occur over HTTP.

Never run either against staging or live.
