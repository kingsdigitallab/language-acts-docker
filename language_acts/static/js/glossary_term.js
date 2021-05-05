const React = window.React;
const Modifier = window.DraftJS.Modifier;
const EditorState = window.DraftJS.EditorState;
const RichUtils = window.DraftJS.RichUtils;

// Since we can't know which page we should use for the snippet
// They should be specificed here
const termURL= '/term/choose/cms/GlossaryTerm/';

//Chooser url: http://127.0.0.1:8000/wagtail/snippets/choose/cms/glossaryterm/

// // Not a real React component – just creates the entities as soon as it is rendered.
// class BibliographictermSource extends React.Component {
//     componentDidMount() {
//         const { editorState, entityType, onComplete } = this.props;
//
//         const content = editorState.getCurrentContent();
//         const selection = editorState.getSelection();
//
//         // Uses the Draft.js API to create a new entity with the right data.
//         const contentWithEntity = content.createEntity(entityType.type, 'MUTABLE');
//         const entityKey = contentWithEntity.getLastCreatedEntityKey();
//
//         // We also add some text for the entity to be activated on.
//         //const text = `$${randomStock}`;
//         const text = '';
//
//         const newContent = Modifier.replaceText(content, selection, text, null, entityKey);
//         const nextState = EditorState.push(editorState, newContent, 'insert-characters');
//
//         onComplete(nextState);
//     }
//
//     render() {
//         return null;
//     }
// }

const filterEntityData = (entityType, data) => {
    let entity_data = {};
    switch (entityType.type) {
        case ("TERM"):
            entity_data = {
                term_id: data.term_id,
            };
            break;

        default:
            break;
    }
    return entity_data;

};

REF_MODEL_CHOOSER_MODAL_ONLOAD_HANDLERS = {
    'choose': function (modal, jsonData) {
        function ajaxifyLinks(context) {
            $('a.snippet-choice', modal.body).on('click', function (event) {
                event.preventDefault();
                // Hijack these snippet edit links and send it to term instad
                let re = /.*\/(\d+)\/$/;
                var found = re.exec($(this).attr('href'));
                modal.loadUrl(termURL+found[1]+'/');

                return false;
            });

            $('.pagination a', context).on('click', function () {
                var page = this.getAttribute('data-page');
                setPage(page);
                return false;
            });
        }

        var searchUrl = $('form.snippet-search', modal.body).attr('action');
        var request;

        function search() {
            request = $.ajax({
                url: searchUrl,
                data: {q: $('#id_q').val(), results: 'true'},
                success: function (data, status) {
                    request = null;
                    $('#search-results').html(data);
                    ajaxifyLinks($('#search-results'));
                },
                error: function () {
                    request = null;
                }
            });
            return false;
        }

        function setPage(page) {
            var dataObj = {p: page, results: 'true'};

            if ($('#id_q').length && $('#id_q').val().length) {
                dataObj.q = $('#id_q').val();
            }

            request = $.ajax({
                url: searchUrl,
                data: dataObj,
                success: function (data, status) {
                    request = null;
                    $('#search-results').html(data);
                    ajaxifyLinks($('#search-results'));
                },
                error: function () {
                    request = null;
                }
            });
            return false;
        }

        $('form.snippet-search', modal.body).on('submit', search);

        $('#id_q').on('input', function () {
            if (request) {
                request.abort();
            }
            clearTimeout($.data(this, 'timer'));
            var wait = setTimeout(search, 200);
            $(this).data('timer', wait);
        });

        ajaxifyLinks(modal.body);
    },
    'chosen': function (modal, jsonData) {
        modal.respond('refChosen', jsonData['result']);
        modal.close();
    }
};


const getChooserConfig = (entityType, entity, selectedText) => {
    let url;
    let urlParams;


    if (entityType.type === 'TERM') {
        let urlParams = {};
        if (selectedText.length > 0){
            // Add the text selection as a default search
            urlParams.q = selectedText;
        }
        return {
            url: termURL,
            urlParams: urlParams,
            onload: REF_MODEL_CHOOSER_MODAL_ONLOAD_HANDLERS,
        };
    } else {
        return {
            url: null,
            urlParams: {},
            onload: {},
        };
    }
};

// https://github.com/wagtail/wagtail/blob/d97f940e58d042ae160be463a14937c1b0ee7718/client/src/components/Draftail/DraftUtils.js

/**
 * Returns collection of currently selected blocks.
 * See https://github.com/jpuri/draftjs-utils/blob/e81c0ae19c3b0fdef7e0c1b70d924398956be126/js/block.js#L19.
 */


const getSelectedBlocksList = (editorState) => {
    const selectionState = editorState.getSelection();
    const content = editorState.getCurrentContent();
    const startKey = selectionState.getStartKey();
    const endKey = selectionState.getEndKey();
    const blockMap = content.getBlockMap();
    const blocks = blockMap
        .toSeq()
        .skipUntil((_, k) => k === startKey)
        .takeUntil((_, k) => k === endKey)
        .concat([[endKey, blockMap.get(endKey)]]);
    return blocks.toList();
};

/**
 * Returns the currently selected text in the editor.
 * See https://github.com/jpuri/draftjs-utils/blob/e81c0ae19c3b0fdef7e0c1b70d924398956be126/js/block.js#L106.
 */


const getSelectionText = (editorState) => {
    const selection = editorState.getSelection();
    let start = selection.getAnchorOffset();
    let end = selection.getFocusOffset();
    const selectedBlocks = getSelectedBlocksList(editorState);

    if (selection.getIsBackward()) {
        const temp = start;
        start = end;
        end = temp;
    }

    let selectedText = '';
    for (let i = 0; i < selectedBlocks.size; i += 1) {
        const blockStart = i === 0 ? start : 0;
        const blockEnd = i === (selectedBlocks.size - 1) ? end : selectedBlocks.get(i).getText().length;
        selectedText += selectedBlocks.get(i).getText().slice(blockStart, blockEnd);
    }

    return selectedText;
};


/**
 * Cloned and modified from ModalWorkflowSource
 * https://github.com/wagtail/wagtail/blob/d97f940e58d042ae160be463a14937c1b0ee7718/client/src/components/Draftail/sources/ModalWorkflowSource.js
 */
class GlossaryTermSource extends React.Component {

    constructor(props) {
        super(props);

        this.onChosen = this.onChosen.bind(this);
        this.onClose = this.onClose.bind(this);
    }

    componentDidMount() {
        const {onClose, entityType, entity, editorState} = this.props;
        const selectedText = getSelectionText(editorState);
        const {url, urlParams, onload} = getChooserConfig(entityType, entity, selectedText);

        $(document.body).on('hidden.bs.modal', this.onClose);

        // let full_url = url+'?q=first';
        // eslint-disable-next-line new-cap
        this.workflow = global.ModalWorkflow({
            url,
            urlParams,
            onload,
            responses: {
                refChosen: this.onChosen,
            },
            onError: () => {
                // eslint-disable-next-line no-alert
                window.alert(STRINGS.SERVER_ERROR);
                onClose();
            },
        });
    }

    componentWillUnmount() {
        this.workflow = null;

        $(document.body).off('hidden.bs.modal', this.onClose);
    }

    onChosen(data) {

        const {editorState, entity, entityKey, entityType, onComplete} = this.props;
        const content = editorState.getCurrentContent();
        const selection = editorState.getSelection();
        const entityData = filterEntityData(entityType, data);
        const mutability = 'IMMUTABLE';

        let nextState;

        const contentWithEntity = content.createEntity(entityType.type, mutability, entityData);
        const newEntityKey = contentWithEntity.getLastCreatedEntityKey();

        const newText = '[ref_' + data.term_id + ']';
        const newContent = Modifier.replaceText(content, selection, newText, null, newEntityKey);
        nextState = EditorState.push(editorState, newContent, 'insert-characters');

        this.workflow.close();

        onComplete(nextState);


    }

    onClose(e) {
        const {onClose} = this.props;
        e.preventDefault();

        onClose();
    }

    render() {
        return null;
    }
}


const GlossaryTerm = (props) => {
    const {entityKey, contentState} = props;
    const data = contentState.getEntity(entityKey).getData();
    return React.createElement('span', {
        'data-term_id': data.term_id,
    }, props.children);
};


window.draftail.registerPlugin({
    type: 'TERM',
    source: GlossaryTermSource,
    decorator: GlossaryTerm,
});
