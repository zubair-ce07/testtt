
import categoryApi from '../api/category';
import {loadCategorySuccess, loadCategoryFailed,
    getPostsSuccess ,getPostsFailed,loadCategoryProgress} from './index';

export function loadCategory() {

    return function(dispatch) {
        dispatch(loadCategoryProgress())

        return categoryApi.getCategoryData().then(categories => {

            dispatch(loadCategorySuccess(categories));

        }).catch(error => {

            dispatch(loadCategoryFailed(error));
        });
    }
}
export function loadPosts(category) {

    return function(dispatch) {
        dispatch(loadCategoryProgress())

        categoryApi.getPostsOfCategory(category).then(posts => {
            console.log(posts)
            dispatch(getPostsSuccess(posts));

        }).catch(error => {

            dispatch(getPostsFailed(error));
        });
    }
}

