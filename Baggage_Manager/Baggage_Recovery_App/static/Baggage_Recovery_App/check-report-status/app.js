window.onload = function () {
  init()
}

function init() {
	var reportId1 = $("#reportId1")
	if (reportId1.length !== 0) {
		var reportId = window.location.href.split("?")[1].split("=")[1]
		reportId1.attr('value', reportId)
	}
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

function redirectToConfirm(e) {
	var url = "confirm-bag-image.html?reportId="
	var card = e.parentNode.parentNode.parentNode
	var reportId = $(card).attr("reportId")
	window.location.replace(url + reportId)
}

function submitError() {
	if (confirm("Are you sure none of these are your bag?")) {
		var reportId = window.location.href.split("?")[1].split("=")[1]
		window.location.replace("submitErrorMatching?reportId=" + reportId)
	}
}

function submitBagImageSelection() {
	var radios = document.getElementsByName('bagImage')
	for (var i = 0, length = radios.length; i < length; i++) {
	  if (radios[i].checked) {
	    var selection = radios[i].value
	    var bagSelection = 'bagSelection=' + selection + '; path=/Baggage_Recovery_App/check-report-status/confirm-bag-content.html'
	    document.cookie = bagSelection
	    var reportId = window.location.href.split("?")[1].split("=")[1]
	    window.location.replace("confirm-bag-content.html?reportId=" + reportId)
	  }
	}
	console.log(bagSelection)
	if (!selection) { alert("please make selection") }
}

function makeSelection(e) {
	if ($(e).dimmer('is active')) {
		$(e).dimmer('hide')
	} else {
		$(e).dimmer('show')
	}
}

function submitContentSelection() {
	var options = $('.content-option')
	var contentSelections = []
	$.each(options, function(i) {
		if ($(options[i]).hasClass('dimmed')) {
			var tmpId = $(options[i]).attr('contentId')
			contentSelections.push(tmpId)
		}
	})
	if (contentSelections.length != 2) {
		alert("Please only select 2 items")
	} else {
		var reportId = window.location.href.split("?")[1].split("=")[1]
		var bagId = getCookie('bagSelection')
		var contentId1 = contentSelections[0]
		var contentId2 = contentSelections[1]
		$("#reportId").attr('value', reportId)
		$("#bagId").attr('value', bagId)
		$("#contentId1").attr('value', contentId1)
		$("#contentId2").attr('value', contentId2)
    $("#userSelections-form").submit()
	}
}
