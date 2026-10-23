<?php
// Formulaire de devis Refreshome — envoi e-mail depuis le serveur (photos jointes) + sauvegarde CSV hors docroot.
// Remplace le formulaire Tally de l'ancien site. Test technique : contact.php?test=1 (envoi à la copie uniquement).
date_default_timezone_set('Europe/Paris');
mb_internal_encoding('UTF-8');

$DEST  = 'mariusvaillant98@gmail.com';            // destinataire visible : le client
$BCC   = 'aymeric@cleanibat.fr';                  // copie cachée Aymeric (et destinataire unique en mode ?test=1)
$FROM  = 'Refreshome <no-reply@refreshome.fr>';   // nécessite le SPF Hostinger sur refreshome.fr (voir README)
$ROOT  = rtrim($_SERVER['DOCUMENT_ROOT'], '/');
$CSV   = dirname($ROOT) . '/leads_refreshome.csv'; // hors docroot
$UPL   = dirname($ROOT) . '/leads_refreshome_photos'; // copies des photos, hors docroot
$THANKS = '/confirmation/';
$TEST  = isset($_GET['test']) && $_GET['test'] === '1';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); header('Content-Type: text/plain; charset=UTF-8'); echo 'Méthode non autorisée.'; exit; }
if (!empty($_POST['_honey'])) { header('Location: ' . $THANKS, true, 303); exit; }

function v($keys){ foreach((array)$keys as $k){ $k2=str_replace([' ','.'],'_',$k);
  foreach([$k,$k2] as $kk){ if(!isset($_POST[$kk])) continue; $x=$_POST[$kk];
    if(is_array($x)) $x=implode(', ', array_map(function($i){return trim(strip_tags((string)$i));}, $x));
    if(trim((string)$x)!=='') return trim(strip_tags((string)$x)); } } return ''; }
$nom=v(['Nom','nom']); $tel=v(['Téléphone','T%C3%A9l%C3%A9phone','telephone']); $email=v(['Email','email']);
$ville=v(['Code postal','Localité','ville']); $besoin=v(['Besoin','besoin']); $delai=v(['Délai','delai']); $org=v(['Entreprise']);
$msg=v(['Message','message']); $src=v(['Source']);

if ($nom==='' || $tel==='' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
  http_response_code(400); header('Content-Type: text/plain; charset=UTF-8');
  echo "Merci de vérifier le nom, le téléphone et l'e-mail, puis de revenir en arrière pour renvoyer le formulaire."; exit;
}

// Photos : 5 max, 8 Mo chacune, images uniquement
$files = [];
if (!empty($_FILES['photos']['name']) && is_array($_FILES['photos']['name'])) {
  $finfo = function_exists('finfo_open') ? finfo_open(FILEINFO_MIME_TYPE) : null;
  foreach ($_FILES['photos']['name'] as $i => $name) {
    if (count($files) >= 5) break;
    if ($_FILES['photos']['error'][$i] !== UPLOAD_ERR_OK || $_FILES['photos']['size'][$i] > 8*1024*1024) continue;
    $tmp = $_FILES['photos']['tmp_name'][$i];
    $mime = $finfo ? finfo_file($finfo, $tmp) : ($_FILES['photos']['type'][$i] ?? '');
    if (strpos($mime, 'image/') !== 0) continue;
    $files[] = ['name' => preg_replace('/[^A-Za-z0-9._-]/', '_', basename($name)), 'mime' => $mime, 'data' => file_get_contents($tmp)];
  }
}

// 1) Filet de sécurité : le lead (et ses photos) est écrit AVANT l'envoi de l'e-mail
$id = date('Ymd-His') . '-' . substr(md5($email . $tel . microtime()), 0, 6);
$fh = @fopen($CSV, 'a');
if ($fh) {
  if (filesize($CSV) === 0) fputcsv($fh, ['date','nom','telephone','email','localite','entreprise','besoin','delai','message','photos','source','test','ip','id'], ';');
  fputcsv($fh, [date('Y-m-d H:i:s'),$nom,$tel,$email,$ville,$org,$besoin,$delai,str_replace(["\r","\n"],' ',$msg),count($files),$src,$TEST?'oui':'',$_SERVER['REMOTE_ADDR']??'',$id], ';');
  fclose($fh); @chmod($CSV, 0600);
}
if ($files && (@is_dir($UPL) || @mkdir($UPL, 0700))) {
  foreach ($files as $k => $f) @file_put_contents("$UPL/$id-$k-{$f['name']}", $f['data']);
}

// 2) E-mail (texte + photos en pièces jointes)
$subject = 'Nouvelle demande de devis – ' . ($besoin !== '' ? $besoin : 'Refreshome') . ($TEST ? ' [TEST]' : '');
$body  = ($TEST ? "*** TEST TECHNIQUE, à ignorer ***\n\n" : '');
$body .= "Nouvelle demande depuis refreshome.fr\n\n";
$body .= "Nom        : $nom\n";
if ($org !== '') $body .= "Entreprise : $org\n";
$body .= "Téléphone  : $tel\nE-mail     : $email\nCode postal: $ville\nPrestation : $besoin\nDélai      : $delai\nPage       : $src\n";
$body .= "Photos     : " . count($files) . "\n\nMessage :\n" . ($msg !== '' ? $msg : '(vide)') . "\n";

$headers  = "From: $FROM\r\nReply-To: =?UTF-8?B?" . base64_encode($nom) . "?= <$email>\r\n";
if (!$TEST) $headers .= "Bcc: $BCC\r\n";
$headers .= "MIME-Version: 1.0\r\n";
if ($files) {
  $b = 'rh_' . md5(uniqid('', true));
  $headers .= "Content-Type: multipart/mixed; boundary=\"$b\"";
  $mail = "--$b\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($body));
  foreach ($files as $f) {
    $mail .= "--$b\r\nContent-Type: {$f['mime']}; name=\"{$f['name']}\"\r\nContent-Transfer-Encoding: base64\r\nContent-Disposition: attachment; filename=\"{$f['name']}\"\r\n\r\n" . chunk_split(base64_encode($f['data']));
  }
  $mail .= "--$b--";
} else {
  $headers .= "Content-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit";
  $mail = $body;
}
$to = $TEST ? $BCC : $DEST;
@mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $mail, $headers);

// 3) Page de confirmation (le lead est déjà sauvegardé même si l'e-mail échoue)
header('Location: ' . $THANKS . '?lp=' . urlencode($src), true, 303);
exit;
