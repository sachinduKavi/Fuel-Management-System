<!DOCTYPE html>
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
    padding-left:10%;
    font-size:50px;
}
td{
    padding:5px;
    padding-left:10px;
}
table
</style>
</head>

<body>
    <h1>Display All Records</h1>
    <table cellspacing='5' id='table1'>
    <tr>
    <th>No</th>
    <th>Page<br>Num</th>
    <th>Registration</th>
    <th width='20%'>Vehicle Type</th>
    <th>Month</th>
    <th>Department</th>
    <th>Diesel</th>
    <th>Petrol</th>
    <th>Amount</th>
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
            echo "<td>OR".$rec_row['or_num']."</td>";
            echo "<td>".$rec_row['pg_num']."</td>";
            echo "<td>".$rec_row['reg_num']."</td>";
            echo "<td>".$rec_row['type']."</td>";
            echo "<td>".$rec_row['month']."</td>";
            echo "<td>".$rec_row['department']."</td>";
            if ($rec_row['fuel_type'] == 'Diesel'){
                echo "<td>".$rec_row['fuel_l']."</td>";
                echo "<td>---</td>";
            }else{
                echo "<td>---</td>";
                echo "<td>".$rec_row['fuel_l']."</td>";
            }
            echo "<td>Rs. ".$rec_row['r_price']."</td>";
            echo "</tr>";
            $count_num += 1;
        }
    }
    echo "<tr>";
    
    ?>
    </table>
</body>
</html>