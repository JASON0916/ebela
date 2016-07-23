jQuery(document).ready(function($) {
    $('#run_spider').click(function () {

        // Ajax POST
        $.ajax({
            url: '/api/spider/run',
            type: 'GET',
            dataType: 'json',
            contentType: "application/json; charset=utf-8",

        })
            .done(function (result) {
                if (result['SUCCESS'] === true) {
                    alert('爬虫已经在运行,请等候一段时间,高频爬取会被禁止')
                } else {
                    // buffer for table items
                    alert('爬虫启动失败')
                }
            });
    });
});
