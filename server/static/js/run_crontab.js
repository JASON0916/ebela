jQuery(document).ready(function($) {
    $('#run_cron').click(function () {
        // get parameters
        var startDate = $('#start-date').val();
        var endDate = $('#end-date').val();

        // Ajax POST
        $.ajax({
            url: '/api/v1.0/run/cron',
            type: 'POST',
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                'startDate': startDate,
                'endDate': endDate
            })
        })
            .done(function (result) {
                if (result['code'] === '301') {
                    window.location = result['redirectUrl'] + window.location.href
                }
                if (result['code'] === '0-000-000') {
                    // buffer for table items
                    alert(result['message'])
                }
            });
    });

    $('#run_dish_rating_cron').click(function () {

        // Ajax POST
        $.ajax({
            url: '/api/v1.0/run/dishRatingCron',
            type: 'POST',
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
            })
        })
            .done(function (result) {
                if (result['code'] === '301') {
                    window.location = result['redirectUrl'] + window.location.href
                }
                if (result['code'] === '0-000-000') {
                    // buffer for table items
                    alert(result['message'])
                }
            });
    })
});
