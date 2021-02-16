var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
      var produkId = this.dataset.produk
      var action = this.dataset.action
      console.log('produkId:',produkId,'action:',action)

      var tes = "AnonymousUser"
      console.log('USER:',user)
      if (user == tes){
        console.log('Not Logged in')
      }else{
        updateUserOrder(produkId, action)
      }
    })
}

function updateUserOrder(produkId, action){
  console.log('User is authenticated, sending data...')

  var url ='/update_item/'

  fetch(url, {
    method: 'POST',
    headers:{
      'Content-Type':'application/json',
      'X-CSRFToken':csrftoken,
    },
    body: JSON.stringify({'produkId':produkId, 'action':action})
  })

  .then((response) =>{
    return response.json()
  })

  .then((data) =>{
    console.log('data:', data)
    location.reload()
  });
}