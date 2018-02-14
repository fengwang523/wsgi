<div id="selectdiv" class="dropdown">
  <hr>
  <h3>Search/Select a Device</h3>
  <input id="deviceinput" list="devicelist" name="devicelist" type="text" required />
  <datalist id="devicelist" >
    <option value="EDTNABXMOT61">
  </datalist>
  <input type="button" id="subscribersbut" onclick="ajaxcall()" value="Ok">
  <p id="selectedp"> Selected: </p>
</div>

<div id="resultdiv" class="resultdiv">
  <hr>
  <h3>Result:</h3>
  <pre id="resultpre" class="resultpre">

  </pre>

</div>

<div id="errordiv" class="errordiv">
  <hr>
  <h3>Errors</h3>
  <pre id="errorpre" class="errorpre">

  </pre>

</div>

<div id="rawdiv" class="rawdiv">
  <hr>
  <h3>Raw SSH Sesstion Output:</h3>
  <pre id="rawpre" class="rawpre">

  </pre>
</div>

<script type="text/javascript">
  //prevent ajax call being cached
  $.ajaxSetup({ cache: false });
  var maindiv = document.getElementById("maindiv")
  maindiv.innerHTML = "<h2>Huawei MA5800-X7 OLT Device Summary Page</h2>";
  var selectdiv = document.getElementById("selectdiv");
  maindiv.appendChild(selectdiv);
  var resultdiv = document.getElementById("resultdiv");
  maindiv.appendChild(resultdiv);
  var errordiv = document.getElementById("errordiv");
  maindiv.appendChild(errordiv);
  var rawdiv = document.getElementById("rawdiv");
  maindiv.appendChild(rawdiv);

/*
  $(document).ready(function() {
    url = "http://abc-ni-01.osc.tac.net/test_wsgi/listdevices";
    url = url + "?type=OT&vendor=Huawei";
    $.ajax({
      headers: {'Cache-Control': 'max-age=0'},
      cache: false,
      type: 'GET',
      url: url,
      success: function(data) {
        for (i = 0; i < data['devices'].length; i++) {
          $("#devicelist").append("<option value='" + data['devices'][i] + "'>");
          //alert(data['devices'][i]);
        }
      },
      error: function(request, status, error) {
        $("#devicelist").append("option value='" + error + "'>");  
      }
    });
  });
*/

  //below has code example how to print JSON data to a tree
  //https://github.com/tamirs9876/JSON.Tree.Builder
  function ajaxcall() {
    //empty current content first
    $("#resultpre").text('');
    $("#errorpre").text('');
    $("#rawpre").text('');

    //construct ajax call url
    url = "http://abc-ni-01.osc.tac.net/test_wsgi/huawei_5800_olt_snapshot";
    url = url + "?device=" + $("#deviceinput").val();

    $("#selectedp").text("Selected: " + $("#deviceinput").val())
    $("#deviceinput").val('')
    
    //$("#resultpre").load(url);
    $.ajax({
      headers: {'Cache-Control': 'max-age=0'},
      cache: false,
      type: 'GET',
      url: url,
      success: function(items) {
        //$.each(items, function(i, item) {
        //)};
        //jsonobj = JSON.parse(items);
        //jsonstr = JSON.stringify(jsonobj);
        //resultpretty = JSON.stringify(items['result'],null,2);
        $("#resultpre").html(items['result']);
        $("#errorpre").text(items['error']);
        $("#rawpre").text(items['raw']);
      },
      error: function(request, status, error) {
		$("#resultpre").text("Error Occured: "  + error + "\nPlease contact NI for help\n");
        //alert(request.responseText);
      }
    });
  }
  
</script>

