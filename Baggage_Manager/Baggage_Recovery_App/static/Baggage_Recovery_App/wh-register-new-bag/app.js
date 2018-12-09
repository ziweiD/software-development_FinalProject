window.onload = function () {
  init()
}

function init() {
  $('.ui.dropdown').dropdown({
    allowAdditions: true,
    forceSelection: true,
    hideAdditions: false
  })

  if ($("#currentBagId").val() != null && $("#currentBagId").val() != ""  && getCookie("currentBagId") != null) {
    var currentBagId = 'currentBagId=' + $("#currentBagId").val() + "; path=/Baggage_Recovery_App/wh-register-new-bag/"
    document.cookie = currentBagId
  } else {
    var currentBagId = getCookie("currentBagId")
    $("#currentBagId").attr("value",currentBagId)
  }

  var validationRules = {
    fields: {
      size: {
        identifier: 'size',
        rules: [
          {
            type   : 'empty',
            prompt : 'Please select a size'
          }
        ]
      },
      color: {
        identifier: 'color',
        rules: [
          {
            type   : 'empty',
            prompt : 'Please select a color'
          }
        ]
      },
      brand: {
        identifier: 'brand',
        rules: [
          {
            type   : 'empty',
            prompt : 'Please select a brand'
          }
        ]
      },
      bagImage: {
        identifier: 'bagImage',
        rules: [
          {
            type   : 'empty',
            prompt : 'Please add a image for the bag'
          }
        ]
      }
    }
  }

  $( 'form' )
    .form( validationRules )
}

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') {
          c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
          return c.substring(name.length, c.length);
      }
  }
  return "";
}

function displayAsImage() {
  var file = $("#bagImageInput")[0].files[0]
  var imgURL = URL.createObjectURL(file),
      img = document.createElement('img');

  img.onload = function() {
    URL.revokeObjectURL(imgURL);
  };

  img.src = imgURL
  $("#preview").empty()
  $("#preview").append(img)
  $(".bottom-fixed-button").removeClass("bottom-fixed-button").addClass("bottom-button")
}

function showExampleImg() {
  $("#exampleImg").css('display', 'block')
}

function hideExampleImg() {
  $("#exampleImg").css('display', 'none')
}

function getMatchResultByBagId() {
  $('.ui .dimmer').dimmer('show')
  $('#loader').addClass('active')
  var url = 'getMatchResultByBag?currentBagId=' + getCookie('currentBagId')
  $.get(url, function(res) {
    var parser = new DOMParser();
    var resAsDom = parser.parseFromString(res, "text/html")
    var newBody = resAsDom.getElementsByTagName("body")[0]
    $('body').replaceWith(newBody)
  })
}

function submitCorrectReport(e) {
  if (confirm("Are you sure this report matches with this bag?")) {
    var card = e.parentNode.parentNode.parentNode
    var reportId = $(card).attr("reportid")
    var bagid = $("#currentBagId").val()
    console.log(bagid)
    var url = 'saveMatchedReport?reportId=' + reportId + '&bagId=' + bagid
    $.get(url, function(res) {
      console.log(res)
      var successMessage =
        `<div class="main">
          <div class="ui positive message">
            <div class="header">
              Your confirmation has been recorded
            </div>
            <p><b>bag ${res.bagId}</b> belongs to <b>report ${res.reportId}</b></p>
          </div>
          <div class="bottom-fixed-button">
            <a class="ui ua-blue fluid circular button" href="../warehouse.html">Back to Homepage</a>
          </div>
        </div>`
      $(".main").replaceWith(successMessage)
    })
  }
}

function submitNoReportsAreCorrect() {
  if (confirm("Are you sure none of these reports match this bag?")) {
    var notFoundMessage =
      `<div class="main">
        <div class="ui warning message">
          <div class="header">
            There is no matching report for this bag.
          </div>
          <ul class="list">
            <li>This is likely because the owner of this bag has not yet filed a report for it.</li>
            <li>This bag will try to be matched as more reports come in.</li>
          </ul>
        </div>
        <div class="bottom-fixed-button">
          <a class="ui ua-blue fluid circular button" href="../warehouse.html">Back to Homepage</a>
        </div>
      </div>`
    $(".main").replaceWith(notFoundMessage)
  }
}
