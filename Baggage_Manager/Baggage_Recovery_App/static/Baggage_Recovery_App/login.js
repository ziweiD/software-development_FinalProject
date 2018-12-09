function submitPassengerId() {
  var pid1 = 'pid=' + $("#passengerId").val() + "; path=/Baggage_Recovery_App/baggage-management/my-baggage.html"
  document.cookie = pid1
	var pid2 = 'pid=' + $("#passengerId").val() + "; path=/Baggage_Recovery_App/missing-report/report-missing-bag.html"
  document.cookie = pid2
  var pid3 = 'pid=' + $("#passengerId").val() + "; path=/Baggage_Recovery_App/index.html"
  document.cookie = pid3
  var MPN = 'MPN=' + $("#passengerId").val() + "; path=/Baggage_Recovery_App/baggage-management/add-new-bag.html"
  document.cookie = MPN
  // TODO: add server-side redirection with auth
  window.location.replace("index.html")
}

function submitEmployeeId() {
	var eid = 'eid=' + $('#employeeId').val()
	document.cookie = eid
	// TODO: add server-side redirection with auth
	window.location.replace("warehouse.html")
}