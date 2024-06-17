<?php
$sys_name = 'OR_SYSTEM_2022';
$conn = new mysqli('localhost', 'root', 'root', $sys_name);
if ($conn->connect_error){
    echo "Error";
}else{
    echo "Connected to $sys_name";
}
?>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8" />
    <title>OR Display</title>

<style>
table{
    width:100%;
    font-size:18px;
    border-color:white;
    margin:0;
}
th{
    background-color:#065C18;
    font-size:20px;
    color:white;
}
h1{
    padding-left:5%;
    font-size:50px;
}
td{
    padding:8px;
    padding-left:10px;
}
tr{
   background-color:#D0DBDA;
}
table
</style>
</head>

<body>
    <h1>Display All Records</h1>
    <table cellspacing='5' id='table1'>
    <tr>
    <th>Page<br>Date</th>
    <th width='7%'>No</th>
    <th>Page<br>Num</th>
    <th width='6%'>Registration</th>
    <th width='25%'>Vehicle Type</th>
    <th>Month</th>
    <th>Department</th>
    <th width='6%'>Rate (Rs.)</th>
    <th width='6%'>Diesel</th>
    <th width='6%'>Petrol</th>
    <th width='9%'>Amount (Rs.)</th>
    </tr>
    <?php
    // Extracting data from database 
    $oil_rec_sql = "SELECT * FROM oil_records INNER JOIN vehicle_register ON reg_num=vehicle_reg ORDER BY or_num DESC";
    $result_rec = $conn->query($oil_rec_sql);
    $count_rec = mysqli_num_rows($result_rec);
    if ($count_rec == true){
        $count_num = 0;
        while($rec_row = $result_rec->fetch_assoc()){
            echo "<tr>";
            echo "<td>OR".$rec_row['dte']."</td>";
            echo "<td>OR".$rec_row['or_num']."</td>";
            echo "<td>".$rec_row['pg_num']."</td>";
            echo "<td>".$rec_row['reg_num']."</td>";
            echo "<td>".$rec_row['type']."</td>";
            echo "<td>".$rec_row['month']."</td>";
            echo "<td style='text-align:right;'>".$rec_row['fuel_price']."</td>";
            if ($rec_row['fuel_type'] == 'Diesel'){
                echo "<td style='text-align:right;'>".$rec_row['fuel_l']."</td>";
                echo "<td style='text-align:right;'>---</td>";
            }else{
                echo "<td style='text-align:right;'>---</td>";
                echo "<td style='text-align:right;'>".$rec_row['fuel_l']."</td>";
            }
            echo "<td style='text-align:right;'>".number_format($rec_row['r_price'], 2)."</td>";
            echo "</tr>";
            $count_num += 1;
        }
    }
    echo "<tr>";
    
    ?>
    </table>
</body>
</html>