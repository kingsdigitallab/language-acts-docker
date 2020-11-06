REF_MODEL_CHOOSER_MODAL_ONLOAD_HANDLERS = {
    'choose': function(modal, jsonData) {
        console.log('setup');
        $('a.snippet-choice').on('click', function (event) {
            /*alert('whee');

            let modelMeta = {'appName': this.dataset.appName, 'modelName': this.dataset.modelName};
            modal.respond('refChoosen', modelMeta);
            modal.close();
            $(".modal-backdrop").remove();*/
            event.preventDefault();
            window.console.log($(this).attr('href'));
            var pageData = $(this).data();
            //pageData.parentId = jsonData['parent_page_id'];
            //modal.respond('pageChosen', pageData);
            //modal.close();
            $(this).attr('href');
            return false;
        });
    }
};
