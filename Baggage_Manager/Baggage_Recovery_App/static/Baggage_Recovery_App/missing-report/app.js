window.onload = function () {
  init()
}

function init() {
  $('.ui.dropdown').dropdown()
  $('.ui.dropdown.brand-dropdown').dropdown({
    allowAdditions: true,
    forceSelection: true,
    hideAdditions: false
  })

	if (getCookie('pid') != '') {
		var pid = getCookie('pid')
		$("#pid").attr("value", pid)
    var url = '../baggage-management/getSavedBags?pid=' + pid + '&reportMissingBag=true'
    $.get(url, function(res) {
      showBags(res)
    })
  }

  var validationRules = {
    fields: {
      confirm_bag_selection: {
        identifier: 'confirm_bag_selection',
        rules: [
          {
            type   : 'empty',
            prompt : 'Please select the missing bag'
          }
        ]
      },
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
      firstName: {
        identifier: 'firstName',
        rules: [
          {
            type   : 'empty',
            prompt : 'Please enter your firstname'
          }
        ]
      },
      lastName: {
        identifier: 'lastName',
        rules: [
          {
            type   : 'empty',
            prompt : 'Please enter your lastname'
          }
        ]
      },
      details: {
        identifier: 'details',
        rules: [
          {
            type   : 'empty',
            prompt : 'Please enter details about items inside the lost bag'
          }
        ]
      },
      permanantAddress: {
        identifier: 'permanantAddress',
        rules: [
          {
            type   : 'empty',
            prompt : 'Please enter your permanant address'
          }
        ]
      },
      temporaryAddress: {
        identifier: 'temporaryAddress',
        rules: [
          {
            type   : 'empty',
            prompt : 'Please enter your temporary address'
          }
        ]
      },
      validBefore: {
        identifier: 'validBefore',
        rules: [
          {
            type   : 'empty',
            prompt : 'Please enter your valid time for your temporary address'
          }
        ]
      }
    }
  }

  $( 'form' )
    .form( validationRules )
    .on( 'change', '[type=radio]', function(e)
    {
        var hidden = $("[type=hidden][name='confirm_bag_selection']")
        hidden.val($(this).val());
    });

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

function showBags(res) {
  var items = ""
  var data = res.data
  $.each(data, function(i, bag) {
    items +=
    `<div class="ui raised card bag-option" bagid="${bag.bagID}"">
      <div class="bag-option-image">
        <img src="${bag.url}">
      </div>
      <div class="bag-option-content">
        <h3 class="bag-option-name">${bag.bagName}</h3>
        <div class="meta">
        	Added on ${bag.time.slice(0, 10)}
          <div class="field">
            <div class="ui radio checkbox">
  					  <input type="radio" id="bag${bag.bagID}" name="missingBag" value="${bag.bagID}">
  					  <label for="bag${bag.bagID}">This bag is lost</label>
  					</div>
          </div>
        </div>
      </div>
    </div>
    `
  })
  $("#bagSelectionContainer").show().fadeIn(1200)
  $("#bag-selection").append(items).fadeIn(1200)
}
