function getReportStatus() {
	var url = "check-report-status/all-reports.html?pid="
	var pid = getCookie('pid')
	window.location.replace(url + pid)
}

function getMyBaggage() {
	var url = 'baggage-management/getSavedBags?pid=' + getCookie('pid')
	window.location.replace(url)
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
