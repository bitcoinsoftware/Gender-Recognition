<?php
if($_SERVER["HTTPS"] != "on") {
   header("HTTP/1.1 301 Moved Permanently");
   header("Location: https://" . $_SERVER["SERVER_NAME"] . $_SERVER["REQUEST_URI"]);
   exit();
}
?>

<html>
<body>
	
<form action="" method="POST">
PASSWORD:<br /> <input type="password" name="pass"  value= "" /><br />
LOGIN:<br /><input type="text" name="log" value= "" />
<input type="submit" value="SUBMIT" /> <input type="reset" value="RESET" />
</form>
	
<?php
	$password = $_POST["pass"];
    echo date("d,h");
    echo "<br/>";
	//$datahs = md5(date("d,h"));
						//piorebitcoinynaokraglo
	if($_POST['pass']=="cb37565bf2cf0c4e0529e1019d358a91")
		{
			 echo "pass OK";
          $datagram = $_POST['log'];
          
          $data_start= substr($datagram, 0,10);
          $data_prefix= substr($datagram,10,3);
          //echo $data_start;
          echo "start";
          echo $data_prefix;
          echo "stop";
          $len = count($datagram);
          if ($data_start == "DATA START"){
            $datagram= substr($datagram,13,$len-9);
            // people_counted, man, woman, av_age, happy, neutral
            if ($data_prefix=="INT"){$url = "locals/Test_Club_in.txt";}
            elseif($data_prefix=="OUT"){$url = "locals/Test_Club_out.txt";}
            if($data_prefix=="INT" || $data_prefix=="OUT")
			{
				$ord_file = fopen($url,"w") or die ("Can't open $filename");
				$fout = fwrite($ord_file, $datagram);
				fclose($ord_file);
			}
          }
		}
	else
		{
			$haselko = "cb37565bf2cf0c4e0529e1019d358a91";
			echo  $haselko;
			echo "<br/>";
			$clear_text_datagram = "DATA START2012-11-04 12:05:01@@@98dce83da57b0395e163467c9dae521b;1LwzehBz13hrFr7Q6uwMBZTNigGiJkvuwr;1.0;1GBrzXGxXT34Ba4Qaw6DURXnpaJWH6YTzr;2.5;24;93;0.0;NOTDATA END";
			echo fnEncrypt($clear_text_datagram, $datahs);	
		}

    function fnEncrypt($sValue, $sSecretKey)
    {
        return trim(
            base64_encode(
                mcrypt_encrypt(
                    MCRYPT_RIJNDAEL_256,$sSecretKey, $sValue, MCRYPT_MODE_ECB, 
                    mcrypt_create_iv(mcrypt_get_iv_size(MCRYPT_RIJNDAEL_256, MCRYPT_MODE_ECB)
                    , MCRYPT_RAND)
                    )
                )
            );
    }

    function fnDecrypt($sValue, $sSecretKey)
    {
        return trim(
            mcrypt_decrypt(
                MCRYPT_RIJNDAEL_256, 
                $sSecretKey, 
                base64_decode($sValue), 
                MCRYPT_MODE_ECB,
                mcrypt_create_iv(
                    mcrypt_get_iv_size(
                        MCRYPT_RIJNDAEL_256,
                        MCRYPT_MODE_ECB
                    ), 
                    MCRYPT_RAND
                )
            )
        );
    }
    ?>



</body>
</html> 
