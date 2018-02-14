<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv='cache-control' content='no-cache'>
  <meta http-equiv='expires' content='0'>
  <meta http-equiv='pragma' content='no-cache'>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  <link rel="stylesheet" href="ops.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
</head>

<body>

<div class="sidenav">
  <a href="index.php?menu=about">About</a>
  <button class="dropdown-btn">Snapshots
    <i class="fa fa-caret-down"></i>
  </button>
  <div class="dropdown-container">
    <a href="#">ISIS</a>
    <a href="#">BGP</a>
    <a href="#">Links</a>
  </div>

  <button class="dropdown-btn">Consumer
    <i class="fa fa-caret-down"></i>
  </button>
  <div class="dropdown-container">
    <a href="index.php?menu=MX_RE_Subscribers">MX_RE</a>
    <a href="index.php?menu=Nokia_RE_Subscribers">Nokia_RE</a>
    <a href="index.php?menu=Cisco_SE_Subscribers">Cisco_SE</a>
  </div>

  <button class="dropdown-btn">Devices
    <i class="fa fa-caret-down"></i>
  </button>
  <div class="dropdown-container">
    <a href="index.php?menu=Huawei_5800_OLT">Huawei_5800_OLT</a>
    <a href="index.php?menu=MX_RE">MX_RE</a>
  </div>

  <a href="index.php?menu=contact">Contact</a>
</div>

<div id="maindiv" class="maindiv">
</div>

<script>
/* Loop through all dropdown buttons to toggle between hiding and showing its dropdown content - This allows the user to have multiple dropdowns without any conflict */
var dropdown = document.getElementsByClassName("dropdown-btn");
var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
}
</script>

<?php
  $menu = $_GET["menu"];
  $menu = basename ($menu);
  if ($menu == "") {
    include "/data/ops/php/about.php";
  } elseif ($menu == "MX_RE_Subscribers") {
    include "/data/ops/php/MX_RE_Subscribers.php";
  } elseif ($menu == "Huawei_5800_OLT") {
    include "/data/ops/php/Huawei_5800_OLT.php";
  } elseif ($menu == "MX_RE") {
    include "/data/ops/php/MX_RE.php";
  } else {
    include "/data/ops/php/about.php";
  }
?>

</body>
</html> 
