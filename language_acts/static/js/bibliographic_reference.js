const React = window.React;
const Modifier = window.DraftJS.Modifier;
const EditorState = window.DraftJS.EditorState;

//Chooser url: http://127.0.0.1:8000/wagtail/snippets/choose/cms/bibliographyentry/

// // Not a real React component – just creates the entities as soon as it is rendered.
// class BibliographicReferenceSource extends React.Component {
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

REF_MODEL_CHOOSER_MODAL_ONLOAD_HANDLERS = {
    'choose': function(modal, jsonData) {
        console.log('setup');
        $('a.snippet-choice').on('click', function (event) {
            /*alert('whee');

            let modelMeta = {'appName': this.dataset.appName, 'modelName': this.dataset.modelName};
            modal.respond('refChoosen', modelMeta);
            modal.close();
            $(".modal-backdrop").remove();*/
            let snippetData = {'href':$(this).attr('href'), 'label': $(this).html()}
            event.preventDefault();
            window.console.log($(this).attr('href'));
            //var pageData = $(this).data();
            //pageData.parentId = jsonData['parent_page_id'];
            modal.respond('refChosen', snippetData);
            modal.close();
            return false;
        });
    }
};

const getChooserConfig = (entityType, entity, selectedText) => {
    let url;
    let urlParams;

    if (entityType.type === 'REF') {
        return {
            url: "/wagtail/snippets/choose/cms/bibliographyentry/",
            urlParams: {},
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

/*
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
*/
/**
 * Returns the currently selected text in the editor.
 * See https://github.com/jpuri/draftjs-utils/blob/e81c0ae19c3b0fdef7e0c1b70d924398956be126/js/block.js#L106.
 */

/*
export const getSelectionText = (editorState) => {
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
*/

/**
 * Cloned and modified from ModalWorkflowSource
 * https://github.com/wagtail/wagtail/blob/d97f940e58d042ae160be463a14937c1b0ee7718/client/src/components/Draftail/sources/ModalWorkflowSource.js
 */
class BibliographicReferenceSource extends React.Component {

    constructor(props) {
        super(props);

        this.onChosen = this.onChosen.bind(this);
        this.onClose = this.onClose.bind(this);
    }

    componentDidMount() {
        const {onClose, entityType, entity, editorState} = this.props;
        // const selectedText = getSelectionText(editorState);
        const selectedText = '';
        const {url, urlParams, onload} = getChooserConfig(entityType, entity, selectedText);

        $(document.body).on('hidden.bs.modal', this.onClose);


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
        const mutability = MUTABILITY[entityType.type];

        let nextState;

        /*
        if (entityType.block) {
            if (entity && entityKey) {
                // Replace the data for the currently selected block
                const blockKey = selection.getAnchorKey();
                const block = content.getBlockForKey(blockKey);
                nextState = DraftUtils.updateBlockEntity(editorState, block, entityData);
            } else {
                // Add new entity if there is none selected
                const contentWithEntity = content.createEntity(entityType.type, mutability, entityData);
                const newEntityKey = contentWithEntity.getLastCreatedEntityKey();
                nextState = AtomicBlockUtils.insertAtomicBlock(editorState, newEntityKey, ' ');
            }
        } else {
            const contentWithEntity = content.createEntity(entityType.type, mutability, entityData);
            const newEntityKey = contentWithEntity.getLastCreatedEntityKey();

            // Replace text if the chooser demands it, or if there is no selected text in the first place.
            const shouldReplaceText = data.prefer_this_title_as_link_text || selection.isCollapsed();
            if (shouldReplaceText) {
                // If there is a title attribute, use it. Otherwise we inject the URL.
                const newText = data.title || data.url;
                const newContent = Modifier.replaceText(content, selection, newText, null, newEntityKey);
                nextState = EditorState.push(editorState, newContent, 'insert-characters');
            } else {
                nextState = RichUtils.toggleLink(editorState, selection, newEntityKey);
            }
        }

        // IE11 crashes when rendering the new entity in contenteditable if the modal is still open.
        // Other browsers do not mind. This is probably a focus management problem.
        // From the user's perspective, this is all happening too fast to notice either way.
        this.workflow.close();

        onComplete(nextState);
         */
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

/*
BibliographicReferenceSource.propTypes = {
    editorState: PropTypes.object.isRequired,
    entityType: PropTypes.object.isRequired,
    entity: PropTypes.object,
    entityKey: PropTypes.string,
    onComplete: PropTypes.func.isRequired,
    onClose: PropTypes.func.isRequired,
};

BibliographicReferenceSource.defaultProps = {
    entity: null,
};*/


const BibliographicReference = (props) => {
    const {entityKey, contentState} = props;
    const data = contentState.getEntity(entityKey).getData();

    return React.createElement('a', {
        role: 'button',
        onMouseUp: () => {
            //window.open(`https://finance.yahoo.com/quote/`);
        },
    }, props.children);
};


window.draftail.registerPlugin({
    type: 'REF',
    source: BibliographicReferenceSource,
    decorator: BibliographicReference,
});
