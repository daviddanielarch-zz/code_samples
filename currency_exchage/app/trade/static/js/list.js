window.onload = function() {
    new Vue({
     el: '#app',
     data: {
        trades: []
     },

     created: function(){
        var that = this;
        axios.get(TRADE_API_URL)
            .then(function (response) {
                response.data.forEach(elem => {
                    elem.sell_amount = Number(elem.sell_amount).toLocaleString(USER_LANGUAGE, { minimumFractionDigits : 2 });
                    elem.buy_amount = Number(elem.buy_amount).toLocaleString(USER_LANGUAGE, { minimumFractionDigits : 2 });
                    elem.rate = Number(elem.rate).toLocaleString(USER_LANGUAGE, { minimumFractionDigits : 2 });
                    elem.date_booked = moment.utc(elem.date_booked).local().format('L LTS');
                });

                that.trades = response.data;
            })
            .catch(function (error) {
                console.log('Error: ' + error);
            });
        }
    });
    document.getElementById("app").classList.remove("d-none");
}