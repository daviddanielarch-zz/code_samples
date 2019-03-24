function getDecimalSeparator(){
    let num = 10.5;
    if (num.toLocaleString(USER_LANGUAGE).indexOf('.') > 0){
        return '.';
    } else {
        return ',';
    }
}

function updateMessageClass(error){
    if (error){
        document.getElementById("alert").classList.add("alert-danger");
        document.getElementById("alert").classList.remove("alert-success");
    } else {
        document.getElementById("alert").classList.add("alert-success");
        document.getElementById("alert").classList.remove("alert-danger");
    }
}

window.onload = function() {
    Vue.use(VueNumeric.default);
    new Vue({
         el: '#app',
         data: {
             message: null,
             messageClass: null,
             sellCurrency: null,
             buyCurrency: null,
             rate: null,
             rateDisplay: null,
             sellAmount: 0.0,
             decimalSeparator: getDecimalSeparator(),
         },
         methods: {
            onSellCurrencyChange: function(event){
                this.sellCurrency = event.target.value;
                if (this.sellCurrency && this.buyCurrency){
                    this.rate = this.getRate();
                }
            },

            onBuyCurrencyChange: function(event){
                this.buyCurrency = event.target.value;
                if (this.sellCurrency && this.buyCurrency){
                    this.rate = this.getRate();
                }
            },

            getRate: function(){
                var that = this;
                axios.get(GET_RATE_URL, {params: {sell_currency: this.sellCurrency, buy_currency: this.buyCurrency}})
                    .then(function (response) {
                        that.rate = response.data.rate;
                        that.rateDisplay = response.data.rate.toLocaleString(USER_LANGUAGE);
                    })
                    .catch(function (error) {
                        that.message = error.request.responseText;
                        updateMessageClass(true);
                    });
            },

            createTrade: function () {
                if (!this.sellCurrency){
                    this.message = "You need to choose a sell currency before creating a trade";
                    updateMessageClass(true);
                } else if (!this.buyCurrency){
                    this.message = "You need to choose a buy currency before creating a trade";
                    updateMessageClass(true);
                } else if (!this.sellAmount){
                    this.message = "0 is not a valid amount to sell";
                    updateMessageClass(true);
                } else {
                    var that = this;
                    axios.post(TRADE_API_URL,
                        {sell_currency: this.sellCurrency, buy_currency: this.buyCurrency, sell_amount: this.sellAmount}
                    )
                        .then(function (response) {
                            that.message = "Trade created succesfully";
                            updateMessageClass(false);
                        })
                        .catch(function (error) {
                            that.message = error.request.responseText;
                            updateMessageClass(true);
                        });
                }
            }
         },
         computed: {
             buyAmount: function(){
                 if (!this.rate){ return null; }
                 let amount = (Number(this.rate) * Number(this.sellAmount));
                 return amount.toLocaleString(USER_LANGUAGE);
             }
         }
    });
    document.getElementById("app").classList.remove("d-none");
};