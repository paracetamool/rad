/**------------добавление tooltip (подсказка)------------------- */
var tooltipOpt = {
    trigger  : 'hover',
    placement: 'auto',
    container: 'body',
};

$(document).ajaxSuccess(() => { $('[data-toggle="tooltip"]').tooltip(tooltipOpt) });

