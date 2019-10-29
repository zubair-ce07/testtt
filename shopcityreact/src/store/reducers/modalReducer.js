import { CHANGE_MODAL_STATE, UPDATE_OPTIONS } from '../actions/actions';


const initState = {
    optionsPending: true,
    optionsError: null,
    options: {
        brandChoices: null,
        sizeChoices: null,
        colourChoices: null,
        categoryChoices: null
    },
    modalOpen: false
};


const modalReducer = (state=initState, action) => {
    switch (action.type){
        case CHANGE_MODAL_STATE:
            return {
                ...state,
                modalOpen: !state.modalOpen
            };
        case UPDATE_OPTIONS:
            return {
                ...state,
                optionsPending: false,
                options: {
                    brandChoices: action.options.brand_choices,
                    sizeChoices: action.options.size_choices,
                    colourChoices: action.options.colour_choices,
                    categoryChoices: action.options.category_choices
                }
            };
    };
    return state;
};

export default modalReducer;
