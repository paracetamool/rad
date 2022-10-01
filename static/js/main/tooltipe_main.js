var tooltipOpt = {
    trigger  : 'hover',
    placement: 'auto',
    container: 'body',
};

$(document).ajaxSuccess(() => { $('[data-toggle="tooltip"]').tooltip(tooltipOpt) });

// $(document).ready(function(){
//     $('[data-toggle="tooltip"]').tooltip(tooltipOpt) 
// })

// $('body').tooltip({
//     trigger  : 'hover',
//     placement: 'auto',
//     container: 'body',
//     selector : '[title]',
// })
