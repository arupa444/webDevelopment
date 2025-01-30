<?php
    if($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['submit'])) {
        $dbc= mysqli_connect('localhost', 'root', '', 'final') or die("Connection Failed:" .mysqli_connect_error());
        
        if(isset($_POST['maggi'])){
            $maggi= $_POST['maggi'];
            $sql= "INSERT INTO maggi (maggi) VALUES ('$maggi')";
            $query = mysqli_query($dbc, $sql);
        }
        if(isset($_POST['pizza'])){
            $pizza= $_POST['pizza'];
            $sql1= "INSERT INTO pizza (PIZZA) VALUES ('$pizza')";
            $query = mysqli_query($dbc, $sql1);
            
        }
        if(isset($_POST['pasta'])){
            $pasta= $_POST['pasta'];
            $sql2= "INSERT INTO pasta (PASTA_NAME) VALUES ('$pasta')";
            $query = mysqli_query($dbc, $sql2);
            
        }
        if(isset($_POST['burger'])){
            $burger= $_POST['burger'];
            $sql3= "INSERT INTO burger (BURGER) VALUES ('$burger')";
            $query = mysqli_query($dbc, $sql3);
            
        }
        if(isset($_POST['fries'])){
            $fries= $_POST['fries'];
            $sql4= "INSERT INTO fries (FRIES) VALUES ('$fries')";
            $query = mysqli_query($dbc, $sql4);
            
        }
        if(isset($_POST['garlicBread'])){
            $garlicBread= $_POST['garlicBread'];
            $sql5= "INSERT INTO garlicBread (garlicBread) VALUES ('$garlicBread')";
            $query = mysqli_query($dbc, $sql5);
            
        }
        if(isset($_POST['sandwiches'])){
            $sandwiches= $_POST['sandwiches'];
            $sql6= "INSERT INTO sandwiches (sandwiches) VALUES ('$sandwiches')";
            $query = mysqli_query($dbc, $sql6);
            
        }
        if(isset($_POST['cornAndNachos'])){
            $cornAndNachos= $_POST['cornAndNachos'];
            $sql7= "INSERT INTO cornAndNachos (cornAndNachos) VALUES ('$cornAndNachos')";
            $query = mysqli_query($dbc, $sql7);
            
        }
        if(isset($_POST['hotBeverages'])){
            $hotBeverages= $_POST['hotBeverages'];
            $sql8= "INSERT INTO hotBeverages (hotBeverages) VALUES ('$hotBeverages')";
            $query = mysqli_query($dbc, $sql8);
        }
        if(isset($_POST['coldCoffee'])){
            $coldCoffee= $_POST['coldCoffee'];
            $sql9= "INSERT INTO coldCoffee (coldCoffee) VALUES ('$coldCoffee')";
            $query = mysqli_query($dbc, $sql9);
        }
        if(isset($_POST['freakSnakes'])){
            $freakSnakes= $_POST['freakSnakes'];
            $sql10= "INSERT INTO freakSnakes (freakSnakes) VALUES ('$freakSnakes')";
            $query = mysqli_query($dbc, $sql10);
        }
        if(isset($_POST['waffles'])){
            $waffles= $_POST['waffles'];
            $sql11= "INSERT INTO waffles (waffles) VALUES ('$waffles')";
            $query = mysqli_query($dbc, $sql11);
        }
        if(isset($_POST['snakes'])){
            $snakes= $_POST['snakes'];
            $sql12= "INSERT INTO snakes (snakes) VALUES ('$snakes')";
            $query = mysqli_query($dbc, $sql12);
        }
        if(isset($_POST['plattersAndCombos'])){
            $plattersAndCombos= $_POST['plattersAndCombos'];
            $sql13= "INSERT INTO plattersAndCombos (plattersAndCombos) VALUES ('$plattersAndCombos')";
            $query = mysqli_query($dbc, $sql13);
        }
        if(isset($_POST['chillers'])){
            $chillers= $_POST['chillers'];
            $sql14= "INSERT INTO chillers (chillers) VALUES ('$chillers')";
            $query = mysqli_query($dbc, $sql14);
        }
        if($query) {
            echo 'Order Successfull';
        }
        else {
            echo 'Error Occurred';
        }
    }
?>