window.onload = function () {
  init()
}

function init() {
  if (getCookie('bagid') != '') {
    var url = 'getSavedBag?bagid=' + getCookie('bagid')
    $.get(url, function(res) {
      console.log(res.bagName)
      $("#bagName").attr("placeholder", res.bagName)
      var imgTag = '<img src=' + res.url + '>'
      $("#oldImage").append(imgTag)
      $("#bagID").attr("value", res.bagID)
    })
  }

  if (getCookie('MPN') != '') {
    var pid = getCookie('MPN')
    $("#pid").attr("value", pid)
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

// ============================================================
// Add new Bag
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

// ============================================================
// Delete Bag
function deleteBag(e) {
  if (confirm("Do you really want to delete this bag?")) {
    var card = e.parentNode.parentNode.parentNode
    var bagID = $(card).attr("bagid")
    $(card).remove()
    var url = "deleteBag?bagid=" + bagID
    $.get(url, function(res) {
      console.log(res)
      if (res.error) {
        var errorMessage =
          `<div class="ui negative message">
            <div class="header">
              Cannot Delete This Bag
            </div>
            <p>${res.error}</p>
          </div>`
      $("#message").replaceWith(errorMessage)
      }
    })
  }
}

// ============================================================
// Edit Bag
function editBag(e) {
  var card = e.parentNode.parentNode.parentNode
  var bagID = $(card).attr("bagid")
  var bagidCookie = "bagid=" + bagID + "; path=/Baggage_Recovery_App/baggage-management/edit-bag.html"
  document.cookie = bagidCookie
  window.location.replace("edit-bag.html")
}
