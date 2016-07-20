jQuery(document).ready(function($) {
  // 设置初始分页
  var limit = 30
  var offset = 0
  var current_page = 1
  var total_page = 1
  // 预加载默认日期
  send_query();
  $('#search').click(function(){
    offset = 0;
    send_query();
  });
  $('#nextPage').click(function(){
    if (current_page < total_page) {
      offset = offset + limit;
      send_query();
    } else {
      alert('已达页尾');
    }
  });
  $('#prevPage').click(function(){
    if (current_page > 1) {
      offset = offset - limit;
      send_query();
    } else {
      alert('已达页头');
    }
  });
  $('#firstPage').click(function(){
    offset = 0;
    send_query();
  });
  $('#lastPage').click(function(){
    offset = (total_page - 1) * limit;
    send_query();
  });

  function send_query() {
    // get parameters
    var startDate = $('#start-date').val();
    var endDate = $('#end-date').val();
    // check if startDate is bigger than endDate
    if(startDate > endDate) {
      alert('起始日期必须小于截至日期');
    }
    var periodType = Number($('input[name="period"]:checked').val());
    // 0x1 for new_user, 0x2 for old_user, 0x3 = 0x1 | 0x2 for all_user
    var userType = 0;
    // exam the validness of date if periodType is week
    if (periodType == 1
        && !(new Date(startDate).getDay() == 1 && new Date(endDate).getDay() == 0)
    ) {
      alert('请选择起始时间为周一，截止时间为周日的时间区间');
      return false;
    }
    // exam if the userType is empty
    if (!$('#new_user').is(':checked') && !$('#old_user').is(':checked')) {
      alert('请选择一个用户类型');
      return false;
    }
    if ($('#new_user').is(':checked')) {
      userType |= 1;
    }
    if ($('#old_user').is(':checked')) {
      userType |= 2;
    }
    // Ajax POST
    $.ajax({
      url: '/api/v1.0/info/order',
      type: 'POST',
      dataType: 'json',
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify({
        'startDate': startDate,
        'endDate': endDate,
        'periodType': periodType,
        'userType': userType,
        'limit': limit,
        'offset': offset
      })
    })
    .done(function(result) {
      if (result['code'] === '301') {
        window.location = result['redirectUrl'] + window.location.href
      }
      if (result['code'] === '0-000-000') {
        // buffer for table items
        var _buffer = new Array();
        $.each(result['data'], function (index, data) {
          var user_info = data['userInfo']
          _buffer.push('<tr>');
          _buffer.push('<td>' + data['date'] + '</td>');
          _buffer.push('<td>' + user_info['userCount'] + '</td>');
          _buffer.push('<td>' + user_info['userProportion'] + '</td>');
          _buffer.push('<td>' + user_info['originalPrice'] + '</td>');
          _buffer.push('<td>' + user_info['sellingPrice'] + '</td>');
          _buffer.push('<td>' + user_info['paymentPrice'] + '</td>');
          _buffer.push('<td>' + user_info['promotionAmount'] + '</td>');
          _buffer.push('<td>' + user_info['promotionRate'] + '</td>');
          _buffer.push('<td>' + user_info['voucherAmount'] + '</td>');
          _buffer.push('<td>' + user_info['voucherRate'] + '</td>');
          _buffer.push('<td>' + user_info['orderDays'] + '</td>');
          _buffer.push('<td>' + user_info['dailyItems'] + '</td>');
          _buffer.push('<td>' + user_info['dailyOriginalPrice'] + '</td>');
          _buffer.push('<td>' + user_info['dailySellingPrice'] + '</td>');
          _buffer.push('<td>' + user_info['dailyPaymentPrice'] + '</td>');
          _buffer.push('<td>' + user_info['orderRate'] + '</td>');
          _buffer.push('<td>' + user_info['userBuyBackRate'] + '</td>');
          _buffer.push('</tr>');
        });
      current_page = result['current_page'];
      total_page = result['total_page'];
      total_count = result['total_count'];
      $('#totalPage').text(total_page);
      $('#currentPage').text(current_page);
      $('#totalRows').text(total_count);
      $('#user_info_table').html(_buffer.join(''));
      }
    });
  }
});
