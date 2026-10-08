<?php
/* Plugin Name: Secure Custom Fields (TEST STUB) */
$GLOBALS['scf_stub'] = ['groups'=>[], 'pages'=>[]];
function acf_add_local_field_group($g){ foreach (['key','title','fields','location'] as $k) if (!isset($g[$k])) throw new Exception("group missing $k"); foreach ($g['fields'] as $f) foreach (['key','name','label','type'] as $k) if (!isset($f[$k])) throw new Exception("field missing $k in ".json_encode($f)); $GLOBALS['scf_stub']['groups'][$g['key']] = $g; }
function acf_add_options_page($p){ $GLOBALS['scf_stub']['pages'][] = $p; }
function update_field($key,$v,$post){ $n = preg_replace('/^field_dd_/','',$key); update_option('options_'.$n,$v); return true; }
function get_field($n,$post){ $v = get_option('options_'.$n, null); return $v === false ? null : $v; }
add_action('init', fn() => do_action('acf/init'), 5);
