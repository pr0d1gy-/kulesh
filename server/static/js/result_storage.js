$(function () {
    var renderRow = function (result) {
        var row = $('<tr data-id="'+result.id +'"></tr>');
        row.append('<td>' + (result.id || '') + '</td>');
        row.append('<td>' + (result.file_name || '') + '</td>');
        row.append('<td>' + (result.task_name || '') + '</td>');
        row.append('<td>' + (result.size || '') + '</td>');
        row.append('<td>' + (result.date_start || '') + '</td>');
        row.append('<td class="delete-result-btn"><span class="btn btn-danger glyphicon glyphicon-trash"></span></td>');
        $('#resultsTable').append(row);
    };
    var renderTable = function (rlist) {
        rlist.forEach(function (result) {
            renderRow(result);
        })
    };

    var initResultList = function(data){
        console.log('data');
        renderTable(data.rlist);
    };

    RequestsResults.getResults(initResultList);
});