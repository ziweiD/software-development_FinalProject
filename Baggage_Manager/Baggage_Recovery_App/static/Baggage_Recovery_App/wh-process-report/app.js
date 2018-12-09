function getDetailsbyBagID(e) {
	var card = e.parentNode.parentNode.parentNode
  var reportId = $(card).attr("reportId")
  var url = "matching-result-by-report.html?reportId=" + reportId
  window.location.replace(url)
}

function submitCorrectReport(e) {
  if (confirm("Are you sure this report matches with this bag?")) {
    var card = e.parentNode.parentNode.parentNode
    var bagId = $(card).attr("bagId")
    var reportId = $("#currentReportId").val()
    var url = '../wh-register-new-bag/saveMatchedReport?reportId=' + reportId + '&bagId=' + bagId
    $.get(url, function(res) {
      var successMessage =
        `<div class="main">
          <div class="ui positive message">
            <div class="header">
              Your confirmation has been recorded!
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

function submitNoBagsAreCorrect() {
  if (confirm("Are you sure none of these bags match this report?")) {
    var notFoundMessage =
      `<div class="main">
        <div class="ui warning message">
          <div class="header">
            There is no matching bag for this report.
          </div>
          <ul class="list">
            <li>This is likely because the missing bag has not arrived the warehouse</li>
        		<li>This report will try to be matched as more bags come in.</li>
          </ul>
        </div>
        <div class="bottom-fixed-button">
          <a class="ui ua-blue fluid circular button" href="../warehouse.html">Back to Homepage</a>
        </div>
      </div>`
    $(".main").replaceWith(notFoundMessage)
  }
}

function closeReport(e) {
	if (confirm("Are you sure you want to mannually close this report?")) {
		var card = e.parentNode.parentNode.parentNode
  	var reportId = $(card).attr("reportId")
  	var url = "../wh-process-report/closeReport?reportId=" + reportId
    console.log(url)
  	$.get(url, function(res) {
  		var closeReportMessage =
      `<div class="ui positive message">
        <div class="header">
          Report ${reportId} has been mannually closed.
        </div>
      </div>`
    $("#message").replaceWith(closeReportMessage)
    card.remove()
  	})
	}
}
