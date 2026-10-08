<?php
// Integration test: real WordPress REST dispatch with HubSpot faked. Needs a local WP with this plugin and
// tests/scf-stub.php (installed as plugins/secure-custom-fields/) active, then: wp eval-file tests/rest-integration.php
// Never run against staging or live: it defines a fake DD_HUBSPOT_TOKEN.
// wp eval-file harness: dispatch real REST requests, fake HubSpot via pre_http_request.
define('DD_HUBSPOT_TOKEN', 'test-token');
$GLOBALS['calls'] = []; $GLOBALS['hs'] = [];   // queue of fake responses
add_filter('pre_http_request', function($pre, $args, $url) {
	$GLOBALS['calls'][] = ['url'=>$url, 'auth'=>$args['headers']['Authorization'] ?? '', 'body'=>json_decode($args['body'], true)];
	$r = array_shift($GLOBALS['hs']) ?? [200, '{}'];
	return ['headers'=>[], 'body'=>$r[1], 'response'=>['code'=>$r[0], 'message'=>''], 'cookies'=>[], 'filename'=>null];
}, 10, 3);
global $wpdb; $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '%dd_rl_%'"); wp_cache_flush();
$fail = 0; function check($n,$ok){ global $fail; echo ($ok?'ok   ':'FAIL ').$n."\n"; $fail |= !$ok; }
function call($body, $nonce = null) {
	$req = new WP_REST_Request('POST', '/dealdirect/v1/submit');
	$req->set_header('content-type','application/json');
	$req->set_header('x-dd-nonce', $nonce ?? wp_create_nonce('dd_submit'));
	$req->set_body(json_encode($body));
	$res = rest_do_request($req); return [$res->get_status(), $res->get_data(), $res->get_headers()];
}
$page = home_url('/offering/riverside-wharf-preferred-equity/');
$reg = ['form'=>'registration','fields'=>['accredited_investor'=>'income','firstname'=>'Ana','lastname'=>'Diaz','email'=>'ana@example.com','phone'=>'3055550100'],
        'consent'=>['agreed'=>true,'text'=>'I consent'],'utm'=>['utm_source'=>'news'],'pageUri'=>$page,'pageName'=>'RW Pref'];

$t = rest_do_request(new WP_REST_Request('GET', '/dealdirect/v1/token'));
check('token route returns a nonce, no-store', $t->get_status()===200 && wp_verify_nonce($t->get_data()['nonce'],'dd_submit') && ($t->get_headers()['Cache-Control'] ?? '')==='no-store, max-age=0');

[$s,$d] = call($reg, 'bogus'); check('bad nonce -> 403, nothing sent', $s===403 && !$GLOBALS['calls']);

[$s,$d,$h] = call($reg);
$c = $GLOBALS['calls'][0] ?? [];
check('registration -> sent', $s===200 && $d['status']==='sent');
check('posted to the Registration form with bearer token', ($c['url']??'')==='https://api.hsforms.com/submissions/v3/integration/secure/submit/2951523/f45b7940-7408-4669-acb0-c38ec1107137' && $c['auth']==='Bearer test-token');
check('payload carries mapped accreditation + utm + pageUri', in_array(['objectTypeId'=>'0-1','name'=>'accredited_investor','value'=>'annual income exceeding $200,000'], $c['body']['fields']) && in_array('utm_source', array_column($c['body']['fields'],'name')) && $c['body']['context']['pageUri']===$page);
check('response not cacheable', ($h['Cache-Control']??'')==='no-store, max-age=0');

$GLOBALS['calls']=[]; $n=$reg; $n['fields']['accredited_investor']='none'; $n['fields']['email']='b@example.com';
[$s,$d] = call($n); check('none of the above -> 422 not_accredited, nothing sent', $s===422 && $d['status']==='not_accredited' && !$GLOBALS['calls']);

$GLOBALS['calls']=[]; $hp=$reg; $hp['website']='spam.example'; $hp['fields']['email']='c@example.com';
[$s,$d] = call($hp); check('honeypot filled -> pretends sent, nothing sent', $s===200 && $d['status']==='sent' && !$GLOBALS['calls']);

$GLOBALS['calls']=[]; $GLOBALS['hs']=[[200,'{"total":0,"results":[]}']];
$or=['form'=>'offering-request','fields'=>['email'=>'new@example.com'],'pageUri'=>$page,'pageName'=>'RW Pref'];
[$s,$d] = call($or); check('offering request, unknown email -> needs_registration, no form post', $d['status']==='needs_registration' && count($GLOBALS['calls'])===1 && str_contains($GLOBALS['calls'][0]['url'],'/crm/v3/objects/contacts/search'));

$GLOBALS['calls']=[]; $GLOBALS['hs']=[[200,'{"total":1,"results":[{"id":"1"}]}'],[200,'{}']]; $or['fields']['email']='known@example.com';
[$s,$d] = call($or); check('offering request, known email -> sent to Offering Request form', $d['status']==='sent' && str_ends_with($GLOBALS['calls'][1]['url'],'3f7d6df4-c356-4d6c-bc04-f9502dd8864b') && !isset($GLOBALS['calls'][1]['body']['legalConsentOptions']));

$GLOBALS['calls']=[]; $GLOBALS['hs']=[[400,'{"errors":[{"message":"Invalid subscription type 3199624"}]}'],[200,'{}']]; $r2=$reg; $r2['fields']['email']='d@example.com';
[$s,$d] = call($r2); $subs2 = array_column($GLOBALS['calls'][1]['body']['legalConsentOptions']['consent']['communications'] ?? [], 'subscriptionTypeId');
check('One to One rejected -> retried without it, sent', $d['status']==='sent' && count($GLOBALS['calls'])===2 && $subs2===[7195048]);

$GLOBALS['calls']=[]; $GLOBALS['hs']=[[400,'{"errors":[{"errorType":"INVALID_EMAIL"}]}']]; $r3=$reg; $r3['fields']['email']='e@example.com';
[$s,$d] = call($r3); check('HubSpot validation error -> 502 with plain message', $s===502 && $d['message']==='Please enter a valid email address.');

$GLOBALS['calls']=[]; $r4=$reg; $r4['fields']['email']='f@example.com'; $r4['pageUri']='https://evil.example/x/';
[$s,$d] = call($r4); check('foreign pageUri -> 400, nothing sent', $s===400 && !$GLOBALS['calls']);

global $wpdb; $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '%dd_rl_%'"); wp_cache_flush(); $GLOBALS["calls"]=[]; $codes=[]; for($i=0;$i<6;$i++){ $x=$reg; $x["fields"]["email"]="same@example.com"; [$s]=call($x); $codes[]=$s; }
echo json_encode($codes),"\n"; check("per-email rate limit kicks in after 4", $codes===[200,200,200,200,429,429]);
exit($fail);
