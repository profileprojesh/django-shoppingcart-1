
let updatebtns = document.getElementsByClassName('update-btn');
for (i = 0; i < updatebtns.length; i++) {
    updatebtns[i].addEventListener('click', function ()

    // if the user is not logged in than show th ealert messagge that he is not logged in
    {
        if (user == 'AnonymousUser') {
            alert("You should be logged in first")

        }

        // if user is logged in than handle the updatecart  info
        else {
            let action = this.dataset.action;
            let product = this.dataset.product;
            url = '/updatecart/'
            data = { 'product': product, 'action': action }
            let params = {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(data)
            }
            fetch(url, params).then((response) => {
                return response.json()
            }).then((data) => {
                let id = `cart-quantity-${data.productid}`
                let btnid = `btn-wrapper-${data.productid}`
                let cart_count = document.getElementById('cart-count')
                let cart_quantity = document.getElementById(id)
                let grand_total = document.getElementById('grand-total')

                // logic for changing the button when the item is added in cart
                let btn_wrapper = document.getElementById(btnid)
                try {
                    btn_wrapper.innerHTML = `<a class = "btn btn-outline-info" href="{% url 'cartsummary' %}">View Cart</a>`;
                }
                catch (error) {
                    console.log(error)
                }

                cart_count.innerHTML = data.cart_size

                try {
                    if (data.quantity == 0) {
                        cart_quantity.parentElement.parentElement.remove()
                        btn_wrapper.innerHTML = `<button class="btn btn-primary update-btn" data-action="add" data-product="${data.productid}">Add to
                        Cart</button>`;


                    }
                    else {
                        cart_quantity.innerHTML = data.quantity
                    }
                    grand_total.innerHTML = data.grandtotal

                }
                catch (err) {
                    console.log(err)


                }


            })

        }

    })
}






function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


