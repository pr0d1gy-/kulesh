$(function () {
    var renderRow = function (task) {
        var row = $('<tr data-id="'+task.id +'"></tr>');
        row.append('<td>' + (task.id || '') + '</td>');
        row.append('<td>' + (task.name || '') + '</td>');
        row.append('<td>' + (task.code_file || '') + '</td>');
        row.append('<td>' + (task.data_file || '') + '</td>');
        row.append('<td>' + (task.updated || '') + '</td>');
        row.append('<td>' + (task.updated || '') + '</td>');
        row.append('<td>' + (task.updated || '') + '</td>');
        //row.append('<td>' + (task.version || '') + '</td>');
        row.append('<td class="run-task-btn"><span class="btn btn-success glyphicon">Run</span></td>');
        row.append('<td class="delete-task-btn"><span class="btn btn-danger glyphicon glyphicon-trash"></span></td>');
        $('#allTasksTable').append(row);
    };
    var renderTable = function (tlist) {
        tlist.forEach(function (task) {
            renderRow(task)
        })
    };

    var initTasksList = function(data){
        renderTable(data.tlist);
        console.log('data ', data)
    };

    RequestsTasks.getTasks(initTasksList);
});
