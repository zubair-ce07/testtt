
import categoryApi from '../api/category';
import {loadCategorySuccess, loadCategoryFailed,
    getPostsSuccess ,getPostsFailed} from './index';

export function loadCategory() {
    return function(dispatch) {

        return categoryApi.getCategoryData().then(categories => {

            dispatch(loadCategorySuccess(categories));

        }).catch(error => {

            dispatch(loadCategoryFailed(error));
        });
    }
}
export function loadPosts(category) {

    return function(dispatch) {

        categoryApi.getPostsOfCategory(category).then(posts => {
            console.log(posts)
            dispatch(getPostsSuccess(posts));

        }).catch(error => {

            dispatch(getPostsFailed(error));
        });
    }
}

