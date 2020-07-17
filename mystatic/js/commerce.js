
$(document).ready(function(){
//contact form handler
var contactForm = $(".contact-form")
var contactFormMethod = contactForm.attr("method")
var contactFormEndpoint=contactForm.attr("action")
function displaySubmitting(submitBtn, defaultText, doSubmit){
  if (doSubmit){
    submitBtn.addClass("disabled")
    submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...")
  }else {
    submitBtn.removeClass("disabled")
    submitBtn.html(defaultText)
  }
  
}


contactForm.submit(function(event){
  event.preventDefault()

  var contactFormSubmitBtn = contactForm.find("[type='submit']")
  var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()


  var contactFormData = contactForm.serialize()
  var thisForm = $(this)
  displaySubmitting(contactFormSubmitBtn, "", true)
  $.ajax({
    method: contactFormMethod,
    url:  contactFormEndpoint,
    data: contactFormData,
    success: function(data){
      contactForm[0].reset()
      $.alert({
        title: "Success!",
        content: data.message,
        theme: "modern",
      })
      setTimeout(function(){
        displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
      }, 1000)
    },
    error: function(error){
      console.log(error.responseJSON)
      var jsonData = error.responseJSON
      var msg = ""

      $.each(jsonData, function(key, value){ // key, value  array index / object
        msg += key + ": " + value[0].message + "<br/>"
      })

      $.alert({
        title: "Oops!",
        content: msg,
        theme: "modern",
      })

      setTimeout(function(){
        displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
      }, 500)

    }
  })
})

//auto search
/*var searchForm = $(".form-search")
var searchInput = searchForm.find("[name='q']")
var typingTimer;
var typingInterval = 500
var searchBtn = searchForm.find("[type='submit']")
searchInput.keyup(function(event){
  clearTimeout(typingTimer)
  typingTimer=setTimeout(performSearch,typingInterval)

})
searchInput.keydown(function(event){
  clearTimeout(typingTimer)
})
function displaySearching(){
  searchBtn.addClass("disabled")
  searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...")
}

function performSearch(){
  displaySearching()
  var query = searchInput.val()
  console.log(query)
  setTimeout(function(){
    window.location.href='search/?q=' + query
  }, 1000)
  
}*/
var productForm=$(".form-product-ajax")
productForm.submit(function(event){
  event.preventDefault();
  console.log("Form is not sending")
  let thisForm = $(this)
  //var actionEndPoint=thisForm.attr("action");
  var actionEndPoint=thisForm.attr("data-endpoint");
  var httpMethod = thisForm.attr("method");
  var formData=thisForm.serialize();
  console.log(formData.cartItemCount)
  $.ajax({
    url:actionEndPoint,
    method:httpMethod,
    data:formData,
    success:function(data){
      var submitSpan=thisForm.find(".submit-span") 
      console.log("success")
      console.log(data.added)
      console.log(data.removed)
      console.log(data.cartItemCount)
      if(data.added){
        submitSpan.html("In cart<button type='submit' class='btn btn-dark'>remove</button>")
      }else{
        submitSpan.html("<button type='submit' class='btn btn-success'>add to cart</button>")
      }
      var navbar = $(".navbar-count")
      console.log(data.cartItemCount)
      navbar.text(data.cartItemCount)
      var currentPath=window.location.href
      console.log(currentPath)
      if(currentPath.indexOf("cart")!==-1){
        refreshCart()
      }
    },
    error:function(errorData){
      $.alert({
              title: "Oops!",
              content: "An error occurred",
              theme: "modern",
            })
    }
  })

})
function refreshCart(){
  console.log("in cart")
  var cartTable = $(".cart-table")
  var cartBody = cartTable.find(".cart-body")
  //cartBody.html("<h1>changed</h1>")
  var productRows = cartBody.find(".cart-product")
  var currentUrl=window.location.href
  var refreshCartUrl ="/api/cart/";
  var refreshCartMethod = "GET";
  var data = {};
  $.ajax({
    url:refreshCartUrl,
    method:refreshCartMethod,
    data:data,
    success:function(data){
      var removeForm=$(".cart-item-remove-form")
      console.log("success")
      console.log(data)
      if(data.products.length > 0){
        productRows.html("")
        i=data.products.length
        $.each(data.products,function(index,value){
          console.log(value)
          var itemRemove = removeForm.clone()
          itemRemove.css("display","block")
          itemRemove.find('.cart-item-product-id').val(value.id)
          cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.name + "</a>" + itemRemove.html() + "</td><td>" + value.price + "</td></tr>")
          i--
        })
        cartBody.find(".cart-subtotal").text(data.subtotal)
        cartBody.find(".cart-total").text(data.total)
      }else{
        window.location.href=currentUrl
      }
    },
    error:function(errorData){
      console.log(errorData)
      $.alert({
              title: "Oops!",
              content: "An error occurred",
              theme: "modern",
            })
    }
  }) 
}
})