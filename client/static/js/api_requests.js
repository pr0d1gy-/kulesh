// Tasks
TasksUrl = {
    Tasks: function(id){
        var url = '/api/tasks/';
        if (id){
            url += id + '/';
        }

        return url;
    },
    RunTasks: function(id){
        url = TasksUrl.Tasks(id);
        url += 'run/';

        return url;
    },
};

RequestsTasks = {
    getToken: function () {
        return $('body').data('token')
    },
    getTasks: function(success, error) {
        $.ajax({
            url: TasksUrl.Tasks(),
            method: 'GET',
            dataType: 'JSON',
            data: {
                'access_token': RequestsTasks.getToken()
            },
            success: success,
            error: error
        })
    },
    createTask: function(data, success){
        data = $.extend({'access_token': RequestsTasks.getToken()}, data );
        $.ajax({
            url: TasksUrl.Tasks(),
            method: 'POST',
            dataType: 'JSON',
            data: data,
            success: success
        });
    },
    deleteTask: function(id, success){
        $.ajax({
            url: TasksUrl.Tasks(id),
            method: 'DELETE',
            dataType: 'JSON',
            data: {
                'access_token': RequestsTasks.getToken()
            },
            success: success
        })
    },
    runTask: function(id, success){
        $.ajax({
            url: TasksUrl.RunTasks(id),
            method: 'GET',
            dataType: 'JSON',
            data: {
                'access_token': RequestsTasks.getToken()
            },
            success: success
        })
    }
};


function getFormData(form){
    var unindexed_array = form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}

$(function() { // getting data for the table
    $('#create_task_form').submit(function (event) {
        event.preventDefault();
        var formData = getFormData($(this));
        console.log(formData);
        RequestsTasks.createTask(formData, function(data){
            if (data.status == 'Success'){
                alert(data.msg);
                $(this).trigger('reset');
            } else if (data.status == 'Error'){
                alert(data.msg);
            } else {
                alert('Something wrong!');
            }
        });
    });



    $('#allTasksTable').delegate('.delete-task-btn', 'click', function () {
        var row =  $(this).parent();
        var success = function () {
            alert("Task was removed.");
            row.remove();
        };
        console.log($(this).parent().data('id'));
        RequestsTasks.deleteTask($(this).parent().data('id'), success)
    });

    $('#allTasksTable').delegate('.run-task-btn', 'click', function () {
        var row =  $(this).parent();
        var success = function () {
            alert("Task has been run.");
        };
        console.log($(this).parent().data('id'));
        RequestsTasks.runTask($(this).parent().data('id'), success)
    });



    var initLeftMenu = function () {
        var currPage = document.location.pathname.replace('/', '');
        $('#'+currPage).addClass('active');
    };
    initLeftMenu()

    $('#resultsTable').delegate('.delete-result-btn', 'click', function () {
        var row =  $(this).parent();
        var success = function () {
            alert("Result was removed.");
            row.remove();
        };
        console.log($(this).parent().data('id'));
        RequestsResults.deleteResults($(this).parent().data('id'), success)
    });

});

// Results
ResultsUrl = {
    Results: function(id){
        var url = '/api/results';
        if (id){
            url += '/' + id;
        }
        return url;
    }
};

RequestsResults = {
    getResults: function (success) {
        $.ajax({
            url: ResultsUrl.Results(),
            method: 'GET',
            dataType: 'JSON',
            data: {
                'access_token': RequestsTasks.getToken()
            },
            success: success
        })
    },

    createResults: function (data) {
        data = $.extend({'access_token': RequestsTasks.getToken()}, data );
        $.ajax({
            url: ResultsUrl.Results(),
            method: 'POST',
            dataType: 'JSON',
            data: data,
            success: function (data) {
                console.log(data);
            }
        })
    },
    deleteResults: function (id, success) {
        $.ajax({
            url: ResultsUrl.Results(id),
            method: 'DELETE',
            dataType: 'JSON',
            data: {
                'access_token': RequestsTasks.getToken()
            },
            success: success
        })
    }
};

