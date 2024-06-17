<!DOCTYPE html>
<?php
$sys_name = "OR_SYSTEM_2022";
$conn = new mysqli('localhost', 'root', 'root', "$sys_name");
$month_list = array('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December');
$month_sin = array('ජනවාරි', 'පෙබරවාරි', 'මාර්තු', 'අප්‍රෙල්', 'මැයි', 'ජුනි', 'ජුලි', 'අගොස්තු', 'සැප්තැම්බර්', 'ඔත්තොබර්', 'නොවැම්බර්', 'දෙසැම්බර්');
if(isset($_POST['arrow_btn'])){
	$month_num = $_POST['m_num'];
	$sign = $_POST['arrow_btn'];
	if($sign == "+" && $month_num < 12){
		$month_num += 1;
	}elseif($sign == "-" && $month_num > 3){
		$month_num -= 1;
	}
}else{
	$month_num = date('m');
}
$c_month = array($month_list[$month_num-3], $month_list[$month_num-2], $month_list[$month_num-1]);
$sin_month = array($month_sin[$month_num-3], $month_sin[$month_num-2], $month_sin[$month_num-1]);

if($conn-> connect_error){
	echo "Error";
}else{
	echo "Connected to ".$sys_name."<br>";
}
?>
<html lang="en">
<head>
<title>Summary Sheet</title>

</head>
<style>
h1{
	font-size:30px;
	margin:auto;
	padding:10px;
	text-align:center;
	text-decoration:underline;
}
table{
	width:100%;
}
td{
	padding:5px;
}
button{
	border-radius:40px;
	border:5px white solid;
}
#signature{
	padding:100px;
	padding-left:40px;
}
#subSign{
	padding-left:10px;
}
</style>
<body>
<h1>නාගරික ඉංජිනේරු දෙපාර්තමේන්තුව - 2022 <?php echo $sin_month[0].', '.$sin_month[1].', '.$sin_month[2]?> මස ඉන්ධන වාර්තාව.</h1>
<table border=3, cellspacing=0>
<tr>
<th rowspan='2'>අනු අංකය</th>
<th rowspan='2'>පිටු අංකය</th>
<th rowspan='2'>වාහන අංකය</th>
<th rowspan='2' width='25%'>වාහන වර්ගය</th>


<form action='summary_report.php', method='post'>
<input type='hidden' name='m_num' value='<?php echo $month_num?>'>
<th colspan='3'>
				<button type='submit' name='arrow_btn' value='-'><<</button>
				<?php echo $sin_month[0]?> මාසය
				<button type='submit' name='arrow_btn' value='+'>>></button>
				</th>
<th colspan='3'>
				<button type='submit' name='arrow_btn' value='-'><<</button>
				<?php echo $sin_month[1]?> මාසය
				<button type='submit' name='arrow_btn' value='+'>>></button>
				</th>
<th colspan='3'>
				<button type='submit' name='arrow_btn' value='-'><<</button>
				<?php echo $sin_month[2]?> මාසය
				<button type='submit' name='arrow_btn' value='+'>>></button>
				</th>

</tr>
<tr>
<th>ඩීසල්<br>ලීටර්</th>
<th>පෙට්‍රොල්<br>ලීටර්</th>
<th>මුදල</th>

<th>ඩීසල්<br>ලීටර්</th>
<th>පෙට්‍රොල්<br>ලීටර්</th>
<th>මුදල</th>

<th>ඩීසල්<br>ලීටර්</th>
<th>පෙට්‍රොල්<br>ලීටර්</th>
<th>මුදල (Rs.)</th>
</tr>
</form>

<?php
// Extracting data from vehicle registry
$veh_rec_sql = "SELECT * FROM vehicle_register ORDER BY reg_num ASC";
$result_veh = $conn -> query($veh_rec_sql);
$count = mysqli_num_rows($result_veh);

if($count == true){
	$count_num = 0;
	while($veh_row = $result_veh->fetch_assoc()){
		$reg_num = $veh_row['reg_num'];
		$count_num += 1;
		$fuel_type = $veh_row['fuel_type'];
		echo "<tr>";
		echo "<td align='center'>".$count_num."</td>";
		echo "<td align='center'>".$veh_row['current_page']."</td>";
		echo "<td>".$reg_num."</td>";
		echo "<td>".$veh_row['type']."</td>";
		
		
		//Extracting oil records from oil_records table
		foreach($c_month as $single_month){
			$sql_oil = "SELECT * FROM oil_records WHERE month='$single_month' AND vehicle_reg='$reg_num'";
			$result_oil = $conn->query($sql_oil);
			$count_oil = mysqli_num_rows($result_oil);
			$total_l = 0;
			$total_amount = 0;
			if($count_oil == true){
				while($row_oil = $result_oil->fetch_assoc()){
					$total_l += $row_oil['fuel_l'];
					$total_amount += $row_oil['r_price'];
				}
			}
			if($fuel_type == "Diesel"){
				echo "<td style='text-align:right;'>".$total_l."</td>";
				echo "<td style='text-align:right;'>--</td>";
			}else if($fuel_type == "Petrol"){
				echo "<td style='text-align:right;'>--</td>";
				echo "<td style='text-align:right;'>".$total_l."</td>";
			}
			echo "<td style='text-align:right;'>".number_format($total_amount, 2)."</td>";
		}

		
	}
}
?>

</table>

<div id='signature'>
.................................................<br>
<div id='subSign'>
නාගරික ඉංජිනේරු,<br>
මහ නගර සභාව,<br>
මීගමුව.
</div>
</div>


</body>
</html>