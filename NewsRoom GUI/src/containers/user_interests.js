import React,{Component} from 'react'
import { connect } from 'react-redux';
import Multiselect from 'react-bootstrap-multiselect';
import _ from 'lodash';
import { reactLocalStorage } from 'reactjs-localstorage';
import { userCategories, allCategories } from '../actions';

class UserInterests extends Component {

    constructor(props){
      super(props);
      this.state = {interests : [], error: false}
      this.generateDropDownValues = this.generateDropDownValues.bind(this);
      this.onException = this.onException.bind(this);
    }

    componentDidMount(){
        const token = reactLocalStorage.get('token', "");
        if (token){
            this.onException(this.props.userCategories(token));
            this.onException(this.props.allCategories());
        }
        else
        {
            this.props.history.push('/login');
        }
    }

    onException(promise) {
        promise.then(() => {
            const dropDownValues = this.generateDropDownValues();
            this.setState({ interests: dropDownValues })
        }).catch(() => {
            this.setState({ error: true })
        });
    }

    handleChange(object){
        const { context: { value, selected } } = object
        const updatedInterests = this.state.interests.map((interest) => {
            if (interest.value == value) {
                interest.selected = selected;
            }
            return interest
        });
        this.setState({ interests: updatedInterests })
    }

    generateDropDownValues() {
        const categories_list = this.props.categories.map(category => {
                return category.name;
        });

        const interests_list = this.props.userInterests.map(interest => {
            return interest.category.name;
        });
        
        const unselected_interests = _.difference(categories_list, interests_list);

        const selectedInterests = interests_list.map(interest => {
            return {value: interest, selected: true}
        });
        const unselectedInterests = unselected_interests.map(interest => {
            return {value: interest, selected: false}
        });

        return  _.union(selectedInterests, unselectedInterests);        
    }

    render () {
        if(this.state.error)
        {
            return(
                <div>
                    <h1>Something went wrong</h1>
                </div>
            );
        }
        
        return (
            <Multiselect 
                onChange={ this.handleChange.bind(this )} 
                data={ this.state.interests } 
                multiple 
                enableCaseInsensitiveFiltering
            />
        );
    }
}

function mapStateToProps({ userInterests, categories }){
    return { userInterests, categories };
}

export default connect(mapStateToProps,{ userCategories, allCategories })(UserInterests);


