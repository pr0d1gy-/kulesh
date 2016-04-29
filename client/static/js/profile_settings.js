var form = null;
var me = null;
$(document).ready(function(){
    form = $('form#frm_profile_edit');
    ProfileRequests.get(render_user);
    form.on('submit', function(e){
        e.preventDefault();
        update_user()
    })
});
var render_user = function(_me){
    me = _me;
    for (var name in me){
        form.find('input[name="' + name + '"]').val(me[name]);
    }
};
var update_user = function(){
    ProfileRequests.update(me.id, get_form_data(form), function(response){
        if (response.status == 'Success'){
            alert(response.msg);
        } else {
            alert('Error');
            console.log(response);
        }
    });
}