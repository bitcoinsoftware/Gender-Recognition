<html>
<header><META HTTP-EQUIV=Refresh CONTENT="10"; URL="http://www.noszkurwa.com/AA_haksiory_tybana/facjata/locals/Test_Club.php"></header>
<body>
<?php

$url_in  = "Test_Club_in.txt";
$url_out = "Test_Club_out.txt";

$in_file = fopen($url_in,"r") or die ("Can't open $url_in");
$f_size = filesize($url_in);
$txt_in = fread($in_file,$f_size);
fclose($in_file);

$out_file = fopen($url_out,"r") or die ("Can't open $url_out");
$f_size = filesize($url_out);
$txt_out = fread($out_file,$f_size);
fclose($out_file);

//COUNTED;MAN;WOMAN;AVARAGE_AGE;NEUTRAL;HAPPY
$income = explode(";",$txt_in);
$outcome= explode(";",$txt_out);

$people_in= $income[0]-$outcome[0];
$man= $income[1]-$outcome[1];
$woman = $income[2]-$outcome[2];
$avarage_age = $income[3];
$neutral=$income[4]-$outcome[4];
$happy=$income[5]-$outcome[5];


echo "There are {$woman} woman and {$man} man in the club\n The avarage age is {$avarage_age}";

?>

</body>
</html> 
