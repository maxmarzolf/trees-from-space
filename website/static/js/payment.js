// The max and min number of photos a customer can purchase
var MIN_SHIRTS = 1;
var MAX_SHIRTS = 10;

var basicPhotoButton = document.getElementById('basic-photo-button');
document
    .getElementById('quantity-input')
    .addEventListener('change', function (evt) {
        // Ensure customers only buy between 1 and 10 photos
        if (evt.target.value < MIN_SHIRTS) {
            evt.target.value = MIN_SHIRTS;
        }
        if (evt.target.value > MAX_SHIRTS) {
            evt.target.value = MAX_SHIRTS;
        }
    });

/* Method for changing the product quantity when a customer clicks the increment / decrement buttons */
var updateQuantity = function (evt) {
    if (evt && evt.type === 'keypress' && evt.keyCode !== 13) {
        return;
    }

    var isAdding = evt && evt.target.id === 'add';
    var inputEl = document.getElementById('quantity-input');
    var currentQuantity = parseInt(inputEl.value);

    document.getElementById('add').disabled = false;
    document.getElementById('subtract').disabled = false;

    // Calculate new quantity
    var quantity = evt
        ? isAdding
            ? currentQuantity + 1
            : currentQuantity - 1
        : currentQuantity;
    // Update number input with new value.
    inputEl.value = quantity;
    // Calculate the total amount and format it with currency symbol.
    var amount = config.unitAmount;
    var numberFormat = new Intl.NumberFormat(i18next.language, {
        style: 'currency',
        currency: config.currency,
        currencyDisplay: 'symbol',
    });
    var parts = numberFormat.formatToParts(amount);
    var zeroDecimalCurrency = true;
    for (var part of parts) {
        if (part.type === 'decimal') {
            zeroDecimalCurrency = false;
        }
    }
    amount = zeroDecimalCurrency ? amount : amount / 100;
    var total = (quantity * amount).toFixed(2);
    var formattedTotal = numberFormat.format(total);

    document
        .getElementById('submit')
        .setAttribute('i18n-options', `{ "total": "${formattedTotal}" }`);
    updateContent('button.submit');

    // Disable the button if the customers hits the max or min
    if (quantity === MIN_SHIRTS) {
        document.getElementById('subtract').disabled = true;
    }
    if (quantity === MAX_SHIRTS) {
        document.getElementById('add').disabled = true;
    }
};

/* Attach method */
Array.from(document.getElementsByClassName('increment-btn')).forEach(
    (element) => {
        element.addEventListener('click', updateQuantity);
    }
);

/* Handle any errors returns from Checkout  */
var handleResult = function (result) {
    if (result.error) {
        var displayError = document.getElementById('error-message');
        displayError.textContent = result.error.message;
    }
};

// Create a Checkout Session with the selected quantity
var createCheckoutSession = function () {
    var inputEl = document.getElementById('quantity-input');
    var quantity = parseInt(inputEl.value);
    var availableSizes = document.getElementById("size");
    var selectedSize = availableSizes.value;
    return fetch('/create-checkout-session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            quantity: quantity,
            locale: i18next.language.toLowerCase().split('-')[0],
            size: selectedSize,
        }),
    }).then(function (result) {
        return result.json();
    });
};

Array.from(document.getElementsByClassName('increment-btn')).forEach(
    (element) => {
        element.addEventListener('click', updateQuantity);
    }
);

/* Get your Stripe publishable key to initialize Stripe.js */
fetch('/config')
    .then(function (result) {
        return result.json();
    })
    .then(function (json) {
        window.config = json;
        var stripe = Stripe(config.publicKey);
        updateQuantity();
        // Setup event handler to create a Checkout Session on submit
        document.querySelector('#submit').addEventListener('click', function (evt) {
            evt.preventDefault();
            var availableSizes = document.getElementById("size");
            var selectedSize = availableSizes.value;
            // TODO: check if available sizes is there
            if (selectedSize.length < 1) {
                document.getElementById('size-error').innerHTML = "Please Select a Size";
                return;
            }
            createCheckoutSession().then(function (data) {
                stripe
                    .redirectToCheckout({
                        sessionId: data.sessionId,
                    })
                    .then(handleResult);
            });
        });
    });

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
var x, i, j, l, ll, selElmnt, a, b, c;
/*look for any elements with the class "sizes":*/
x = document.getElementsByClassName("sizes");
l = x.length;
for (i = 0; i < l; i++) {
    selElmnt = x[i].getElementsByTagName("select")[0];
    ll = selElmnt.length;
    /*for each element, create a new DIV that will act as the selected item:*/
    a = document.createElement("DIV");
    a.setAttribute("class", "select-selected");
    a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
    x[i].appendChild(a);
    /*for each element, create a new DIV that will contain the option list:*/
    b = document.createElement("DIV");
    b.setAttribute("class", "select-items select-hide");
    for (j = 1; j < ll; j++) {
        /*for each option in the original select element,
        create a new DIV that will act as an option item:*/
        c = document.createElement("DIV");
        c.innerHTML = selElmnt.options[j].innerHTML;
        c.addEventListener("click", function (e) {
            /*when an item is clicked, update the original select box,
            and the selected item:*/
            var y, i, k, s, h, sl, yl;
            s = this.parentNode.parentNode.getElementsByTagName("select")[0];
            sl = s.length;
            h = this.parentNode.previousSibling;
            for (i = 0; i < sl; i++) {
                if (s.options[i].innerHTML == this.innerHTML) {
                    s.selectedIndex = i;
                    h.innerHTML = this.innerHTML;
                    y = this.parentNode.getElementsByClassName("same-as-selected");
                    yl = y.length;
                    for (k = 0; k < yl; k++) {
                        y[k].removeAttribute("class");
                    }
                    this.setAttribute("class", "same-as-selected");
                    break;
                }
            }
            h.click();
        });
        b.appendChild(c);
    }
    x[i].appendChild(b);
    a.addEventListener("click", function (e) {
        /*when the select box is clicked, close any other select boxes,
        and open/close the current select box:*/
        e.stopPropagation();
        closeAllSelect(this);
        this.nextSibling.classList.toggle("select-hide");
        this.classList.toggle("select-arrow-active");
        document.getElementById('size-error').innerHTML = "";
    });
}

function closeAllSelect(elmnt) {
    /*a function that will close all select boxes in the document,
    except the current select box:*/
    var x, y, i, xl, yl, arrNo = [];
    x = document.getElementsByClassName("select-items");
    y = document.getElementsByClassName("select-selected");
    xl = x.length;
    yl = y.length;
    for (i = 0; i < yl; i++) {
        if (elmnt == y[i]) {
            arrNo.push(i)
        } else {
            y[i].classList.remove("select-arrow-active");
        }
    }
    for (i = 0; i < xl; i++) {
        if (arrNo.indexOf(i)) {
            x[i].classList.add("select-hide");
        }
    }
}

/*if the user clicks anywhere outside the select box,
then close all select boxes:*/
document.addEventListener("click", closeAllSelect);